import re

from .langdata import get_code
from .theme import prettify


def print_welcome():
    print(prettify('shell-announcement', 'Welcome to the translator shell!'))


def print_bye():
    print(prettify('shell-announcement', 'Goodbye.'))


def command_error(text):
    print(prettify('shell-command-error', text))


def command_success(text):
    print(prettify('shell-command-success', text))


def prompt() -> str:
    while True:
        try:
            return input('> ').lstrip()
        except InterruptedError:
            print_bye()
            exit(130)
        except UnicodeDecodeError as e:
            command_error(f'It appears you have entered invalid characters:\n{e.reason}\n\n'
                          f'If your intention was to quit the shell, please enter :q')


# Initialize Translation Engine
# Initialize Audio/Fribidi/Misc
# Print Welcome
# 1. Prompt
# 2. Detect command
# 2.1. Execute command, go to 1
# 3. Send to translation engine
# 4. Print tty output
# 5. Play audio if enabled
# 6. Check option repeat-tty-capture
# 6.1. Capture tty
# 6.2. Detect command
# 6.2.1. Execute command such as Repeat audio, go to 6.2
# 6.3. Uncapture tty
# 7. Clean up, go to 1


class InteractiveShell:
    def __init__(self, cli: "TranslationCLI"):
        self.cli = cli

    def run_interactive(self) -> int:
        print_welcome()
        self.show_settings()
        while True:
            user_input = prompt()
            if user_input.startswith(':'):
                self.execute_command(user_input)
                continue

            user_input = self.try_process_language_prefix(user_input)

            if user_input:
                translation = self.cli.engine.translate(user_input, self.cli.options.source_lang)
                #print(translation.)

        print("Interactive mode would be implemented here")
        return 0

    def execute_command(self, user_input):
        command, *args = user_input[1:].split()

        if command in ('q', 'quit'):
            print_bye()
            exit(0)
        elif command == 'show':
            self.show_settings()
        elif command == 'engine':
            if len(args) < 1:
                command_error('Missing required argument: <engine>')
                return
            self.set_engine(args[0])
        elif command == 'set':
            if len(args) < 1:
                command_error('Missing required argument: <langs>')
                return
            if self.set_languages(args[0]):
                command_success(f'{self.cli.options.source_lang} -> {'+'.join(self.cli.options.target_langs)}')
        elif command in ('s', 'swap'):
            self.swap_languages()
        elif command == 'mute':
            self.set_audio_mode(0)
        elif command == 'play':
            self.set_audio_mode(1)
        elif command == 'speak':
            self.set_audio_mode(2)
        elif command in ('r', 'repeat'):
            self.repeat_audio()
        elif command == 'brief':
            self.set_verbose(False)
        elif command == 'verbose':
            self.set_verbose(True)
        else:
            command_error(f'Unknown command: {command}')

    def show_settings(self):
        text = (f'Engine:  {self.cli.options.engine}\n'
                f'Langs:   {self.cli.options.source_lang} -> {'+'.join(self.cli.options.target_langs)}\n'
                f'Audio:   {['off', 'play', 'speak'][self.cli.options.audio_mode]}\n'
                f'Verbose: {'yes' if self.cli.options.verbose else 'no'}')
        print(prettify('shell-announcement', text))

    def set_engine(self, engine):
        if engine not in self.cli.engines:
            command_error(f'Unknown engine: {engine}')
        else:
            self.cli.options.engine = engine
            self.cli.init_engine()
            command_success(f'Changed translation engine to {engine}')

    def set_languages(self, lang_input):
        if match := re.compile(self.language_pattern()).search(lang_input):
            source, targets = match.group(1), match.group(3).split('+')
            if not get_code(source.removeprefix('@')):
                command_error(f'Unknown source language: {source}')
                return False
            for target in targets:
                if not get_code(target.removeprefix('@')):
                    command_error(f'Unknown target language: {target}')
                    return False
            self.cli.options.source_lang = source
            self.cli.options.target_langs = targets
            return True
        else:
            command_error(f'Invalid language string: {lang_input}')
            return False

    def swap_languages(self):
        if self.cli.options.source_lang == 'auto':
            command_error('Cannot swap, because source language is \'auto\'')
            return
        # If there is more than one target language, move source to the end of the target list and make the first target
        # lang the new source lang. This effectively cycles through the target language list.
        self.cli.options.target_langs.append(self.cli.options.source_lang)
        self.cli.options.source_lang = self.cli.options.target_langs.pop(0)
        command_success(f'{self.cli.options.source_lang} -> {'+'.join(self.cli.options.target_langs)}')

    def set_audio_mode(self, mode):
        self.cli.options.audio_mode = mode
        command_success('Audio mode set')

    def repeat_audio(self):
        pass

    def set_verbose(self, is_verbose: bool):
        self.cli.options.verbose = is_verbose

    def try_process_language_prefix(self, user_input) -> str | None:
        if match := re.match(self.language_pattern(), user_input):
            if self.set_languages(match.group()):
                return user_input[match.end():].lstrip()
            else:
                return None

        return user_input

    @staticmethod
    def language_pattern() -> str:
        # Match patterns like de:@es+fr
        lang_code = r'@?[a-z]{2,3}(-[a-zA-Z]{2,4})?'  # e.g., "en", "en-US"
        lang_chain = rf'({lang_code}\+)*{lang_code}'  # e.g., "en+fr+de"
        return f'^({lang_code})?[:=]({lang_chain})'


def run_emacs_mode() -> int:
    print("Emacs mode would be implemented here")
    return 0
