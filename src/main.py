#!/usr/bin/env python3

import argparse
import os
import sys
from typing import List, Optional, Dict

from src.config import load_init_script
from src.engines.google_translate import GoogleTranslationEngine
from src.interactive import run_interactive, run_emacs_mode
from src.misc import _yn_to_bool, _get_user_lang, _parse_language_codes, _parse_shortcut_format
from src.translate import TranslationEngine
from src.unimpl import _get_version


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with default values"""
    parser = argparse.ArgumentParser(
        prog='trans',
        description='Command-line translation tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False  # We'll handle help ourselves
    )

    # Get default values
    default_width = int(os.environ.get('COLUMNS', 0)) - 2 if os.environ.get('COLUMNS') else 0
    default_user_lang = _get_user_lang()
    default_user_agent = (os.environ.get('USER_AGENT') or
                         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/104.0.0.0 '
                         'Safari/537.36 '
                         'Edg/104.0.1293.54')

    # Information options
    info_group = parser.add_argument_group('Information Options')
    info_group.add_argument('-V', '--version', action='store_const',
                            const='version', dest='info_only',
                            help='Show version information')
    info_group.add_argument('-H', '--help', action='store_const',
                            const='help', dest='info_only',
                            help='Show help message')
    info_group.add_argument('-M', '--man', '--manual', action='store_const',
                            const='manual', dest='info_only',
                            help='Show manual page')
    info_group.add_argument('-T', '--reference', action='store_const',
                            const='reference', dest='info_only',
                            help='Show language reference')
    info_group.add_argument('-R', '--reference-english', action='store_const',
                            const='reference-english', dest='info_only',
                            help='Show language reference in English')
    info_group.add_argument('-S', '--list-engines', action='store_const',
                            const='list-engines', dest='info_only',
                            help='List available translation engines')
    info_group.add_argument('--list-languages', action='store_const',
                            const='list-languages', dest='info_only',
                            help='List available languages')
    info_group.add_argument('--list-languages-english', action='store_const',
                            const='list-languages-english', dest='info_only',
                            help='List available languages in English')
    info_group.add_argument('--list-codes', action='store_const',
                            const='list-codes', dest='info_only',
                            help='List language codes')
    info_group.add_argument('--list-all', action='store_const',
                            const='list-all', dest='info_only',
                            help='List all language information')
    info_group.add_argument('-L', '--linguist', nargs='?', const='',
                            metavar='CODES', dest='linguist_codes',
                            help='Show linguist information for language codes')
    info_group.add_argument('-U', '--upgrade', action='store_const',
                            const='upgrade', dest='info_only',
                            help='Upgrade the program')
    info_group.add_argument('-N', '--nothing', action='store_const',
                            const='nothing', dest='info_only',
                            help='Do nothing')

    # Translator options
    trans_group = parser.add_argument_group('Translator Options')
    trans_group.add_argument('-e', '--engine', metavar='ENGINE', default='google',
                             help='Translation engine to use (default: google)')

    # Display options
    display_group = parser.add_argument_group('Display Options')
    display_group.add_argument('--verbose', action='store_true', default=True,
                               help='Verbose output (default)')
    display_group.add_argument('-b', '--brief', action='store_true', default=False,
                               help='Brief output')
    display_group.add_argument('-d', '--dictionary', action='store_true', default=False,
                               help='Show dictionary entries')
    display_group.add_argument('--identify', action='store_true', default=False,
                               help='Language identification mode')
    display_group.add_argument('--show-original', metavar='Y/n', default='Y',
                               help='Show original text (default: Y)')
    display_group.add_argument('--show-original-phonetics', metavar='Y/n', default='Y',
                               help='Show original phonetics (default: Y)')
    display_group.add_argument('--show-translation', metavar='Y/n', default='Y',
                               help='Show translation (default: Y)')
    display_group.add_argument('--show-translation-phonetics', metavar='Y/n', default='Y',
                               help='Show translation phonetics (default: Y)')
    display_group.add_argument('--show-prompt-message', metavar='Y/n', default='Y',
                               help='Show prompt message (default: Y)')
    display_group.add_argument('--show-languages', metavar='Y/n', default='Y',
                               help='Show languages (default: Y)')
    display_group.add_argument('--show-original-dictionary', metavar='y/N', default='N',
                               help='Show original dictionary (default: N)')
    display_group.add_argument('--show-dictionary', metavar='Y/n', default='Y',
                               help='Show dictionary (default: Y)')
    display_group.add_argument('--show-alternatives', metavar='Y/n', default='Y',
                               help='Show alternatives (default: Y)')
    display_group.add_argument('-w', '--width', type=int, metavar='NUM', default=default_width,
                               help=f'Output width (default: {default_width})')
    display_group.add_argument('--indent', type=int, metavar='NUM', default=4,
                               help='Indentation (default: 4)')
    display_group.add_argument('--theme', metavar='FILENAME', default='default',
                               help='Theme file (default: default)')
    display_group.add_argument('--no-theme', action='store_true', default=False,
                               help='Disable theme')
    display_group.add_argument('--no-ansi', action='store_true', default=False,
                               help='Disable ANSI escape codes')
    display_group.add_argument('--no-autocorrect', action='store_true', default=False,
                               help='Disable autocorrection')
    display_group.add_argument('--no-bidi', action='store_true', default=False,
                               help='Disable bidirectional text')
    display_group.add_argument('--bidi', action='store_true', default=False,
                               help='Force bidirectional text')
    display_group.add_argument('--no-warn', action='store_true', default=False,
                               help='Disable warnings')
    display_group.add_argument('--dump', action='store_true', default=False,
                               help='Dump raw output')

    # Audio options
    audio_group = parser.add_argument_group('Audio Options')
    audio_group.add_argument('-p', '--play', action='store_const', const=1, dest='play_mode',
                             default=0, help='Play audio')
    audio_group.add_argument('--speak', action='store_const', const=2, dest='play_mode',
                             help='Speak translation')
    audio_group.add_argument('-n', '--narrator', metavar='VOICE', default='female',
                             help='Voice for narration (default: female)')
    audio_group.add_argument('--player', metavar='PROGRAM', default=os.environ.get('PLAYER'),
                             help='Audio player program')
    audio_group.add_argument('--no-play', action='store_const', const=0, dest='play_mode',
                             help='Disable audio playback')
    audio_group.add_argument('--no-translate', action='store_true', default=False,
                             help='Skip translation, only play audio')
    audio_group.add_argument('--download-audio', action='store_true', default=False,
                             help='Download audio file')
    audio_group.add_argument('--download-audio-as', metavar='FILENAME',
                             help='Download audio as specific filename')
    audio_group.add_argument('--repeat-tty-capture', action='store_true', default=False,
                             help='Repeat TTY capture')

    # Terminal paging and browsing
    term_group = parser.add_argument_group('Terminal Options')
    term_group.add_argument('-v', '--view', action='store_true', default=False,
                            help='View output in pager')
    term_group.add_argument('--pager', metavar='PROGRAM', default=os.environ.get('PAGER'),
                            help='Pager program')
    term_group.add_argument('--no-view', '--no-pager', action='store_true', default=False,
                            help='Disable pager')
    term_group.add_argument('--browser', metavar='PROGRAM', default=os.environ.get('BROWSER'),
                            help='Browser program')
    term_group.add_argument('--no-browser', action='store_true', default=False,
                            help='Disable browser')

    # Networking options
    net_group = parser.add_argument_group('Networking Options')
    net_group.add_argument('-x', '--proxy', metavar='HOST:PORT',
                           default=os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy'),
                           help='HTTP proxy')
    net_group.add_argument('-u', '--user-agent', metavar='STRING', default=default_user_agent,
                           help='User agent string')
    net_group.add_argument('-4', '--ipv4', '--inet4-only', action='store_const',
                           const=4, dest='ip_version', default=0,
                           help='Use IPv4 only')
    net_group.add_argument('-6', '--ipv6', '--inet6-only', action='store_const',
                           const=6, dest='ip_version',
                           help='Use IPv6 only')

    # Interactive shell options
    shell_group = parser.add_argument_group('Interactive Shell Options')
    shell_group.add_argument('-I', '--interactive', '--shell', action='store_true', default=False,
                             help='Interactive shell mode')
    shell_group.add_argument('-E', '--emacs', action='store_true', default=False,
                             help='Emacs front-end mode')
    shell_group.add_argument('--no-rlwrap', action='store_true', default=False,
                             help='Disable rlwrap')

    # I/O options
    io_group = parser.add_argument_group('I/O Options')
    io_group.add_argument('-i', '--input', metavar='FILENAME',
                          help='Input file')
    io_group.add_argument('-o', '--output', metavar='FILENAME', default=sys.stdout,
                          help='Output file')

    # Language options
    lang_group = parser.add_argument_group('Language Options')
    lang_group.add_argument('--hl', '--host', metavar='CODE', dest='host_lang',
                            default=(os.environ.get('HOST_LANG') or
                                    os.environ.get('HOME_LANG') or
                                    default_user_lang),
                            help='Host language')
    lang_group.add_argument('-s', '--sl', '--source', '-f', '--from',
                            metavar='CODES', dest='source_langs',
                            default=os.environ.get('SOURCE_LANG', 'auto'),
                            help='Source language(s)')
    lang_group.add_argument('-t', '--tl', '--target', '--to',
                            metavar='CODES', dest='target_langs',
                            default=os.environ.get('TARGET_LANG') or default_user_lang,
                            help='Target language(s)')

    # Text preprocessing
    preproc_group = parser.add_argument_group('Text Preprocessing Options')
    preproc_group.add_argument('-j', '--join-sentence', action='store_true', default=False,
                               help='Join sentences')

    # Other options
    other_group = parser.add_argument_group('Other Options')
    other_group.add_argument('-D', '--debug', action='store_true', default=False,
                             help='Debug mode')
    other_group.add_argument('--no-init', action='store_true', default=False,
                             help='Skip initialization script')
    other_group.add_argument('--no-op', action='store_true', default=False,
                             help='No operation')

    # Positional arguments (text to translate and shortcut formats)
    parser.add_argument('text', nargs='*', help='Text to translate or language shortcuts')

    return parser


def _handle_special_args(args: List[str]) -> List[str]:
    """Handle special argument formats before parsing"""
    processed_args = []
    i = 0

    while i < len(args):
        arg = args[i]

        # Handle shortcut format for engines: '/ENGINE'
        if arg.startswith('/') and len(arg) > 1:
            processed_args.extend(['--engine', arg[1:]])
            i += 1
            continue

        # Handle shortcut format for languages: 'CODE:CODE' or 'CODE=CODE'
        lang_shortcut = _parse_shortcut_format(arg)
        if lang_shortcut:
            if 'sls' in lang_shortcut:
                processed_args.extend(['--source', '+'.join(lang_shortcut['sls'])])
            if 'tl' in lang_shortcut:
                processed_args.extend(['--target', '+'.join(lang_shortcut['tl'])])
            i += 1
            continue

        processed_args.append(arg)
        i += 1

    return processed_args


def _post_process_options(options) -> argparse.Namespace:
    """Post-process options after parsing"""

    # TODO: move to info only handling
    if hasattr(options, 'linguist_codes') and options.linguist_codes is not None:
        info_only = 'language'
        if options.linguist_codes:
            options.target_langs = options.linguist_codes
        return options # TODO: weird early return

    # Handle brief mode
    if options.brief:
        options.verbose = False

    # Handle dictionary mode
    if options.dictionary:
        options.show_original_dictionary = True
        options.show_dictionary = False
        options.show_alternatives = False

    # Handle identify mode
    if options.identify:
        options.verbose = max(0, getattr(options, 'verbose', 1) - 2)

    # Handle theme disable
    if options.no_theme:
        options.theme = ''

    # Handle Y/n options conversion
    yn_options = [
        'show_original', 'show_original_phonetics', 'show_translation',
        'show_translation_phonetics', 'show_prompt_message', 'show_languages',
        'show_original_dictionary', 'show_dictionary', 'show_alternatives'
    ]

    for opt in yn_options:
        value = getattr(options, opt.replace('-', '_'), None)
        if isinstance(value, str):
            setattr(options, opt.replace('-', '_'), _yn_to_bool(value))

    # Handle view disable
    if options.no_view:
        options.view = False

    # Handle browser disable
    if options.no_browser:
        options.browser = None

    # Parse language codes
    if isinstance(options.source_langs, str):
        options.source_langs = _parse_language_codes(options.source_langs)
    else:
        options.source_langs = options.source_langs or ['auto']

    if isinstance(options.target_langs, str):
        options.target_langs = _parse_language_codes(options.target_langs)
    else:
        options.target_langs = options.target_langs or [_get_user_lang()]

    # Handle download audio as
    if options.download_audio_as:
        options.download_audio = True

    # Handle narrator/player with play mode
    if (options.narrator != 'female' or options.player) and options.play_mode == 0:
        options.play_mode = 1

    return options


def parse_args(args: Optional[List[str]]) -> argparse.Namespace:
    parser = create_parser()
    args = _handle_special_args(args)
    parsed_args = parser.parse_args(args)
    parsed_args = _post_process_options(parsed_args)
    return parsed_args


class TranslationCLI:
    """Main translation CLI class"""

    def __init__(self):
        self.exit_code = 0
        self.options = None
        self.engine: Optional[TranslationEngine] = None
        self.engines: Dict[str, type[TranslationEngine]] = {
            'google': GoogleTranslationEngine
        }

    def _init_misc(self):
        """Initialize miscellaneous settings"""
        # Set screen width if not already set
        if not self.options.width:
            try:
                import subprocess
                result = subprocess.run(['tput', 'cols'], capture_output=True, text=True)
                if result.returncode == 0:
                    width = int(result.stdout.strip())
                    self.options.width = max(width - 2, 64)
            except:
                self.options.width = 64

        # Initialize browser if not set
        if not self.options.browser:
            import platform
            system = platform.system()
            self.options.browser = 'open' if system == 'Darwin' else 'xdg-open'

    def _handle_info_request(self) -> int:
        """Handle information-only requests"""
        if self.info_only == 'version':
            print(_get_version())
        elif self.info_only == 'help':
            parser = create_parser()
            print(parser.format_help())
        elif self.info_only == 'manual':
            self._show_manual()
        elif self.info_only == 'reference':
            print(self._get_reference('endonym'))
        elif self.info_only == 'reference-english':
            print(self._get_reference('name'))
        elif self.info_only == 'list-engines':
            self._list_engines()
        elif self.info_only == 'list-languages':
            self._list_languages()
        elif self.info_only == 'list-languages-english':
            self._list_languages_english()
        elif self.info_only == 'list-codes':
            self._list_codes()
        elif self.info_only == 'list-all':
            self._list_all()
        elif self.info_only == 'language':
            print(self._get_language_info(self.options.tl))
        elif self.info_only == 'upgrade':
            self._upgrade()
        elif self.info_only == 'nothing':
            pass
        return self.exit_code

    def run_single(self) -> int:
        text_args = self.options.text if hasattr(self.options, 'text') else []

        if len(text_args) > 1 and self.options.join_sentence:
            text_args = [' '.join(text_args)]

        if text_args:
            for i, text in enumerate(text_args):
                if self.options.verbose and i > 0:
                    # Print separator between sources
                    print('-' * (self.options.width or 50))
                self.engine.translate_from_all_source_langs(text, inline=True)
        else:
            # Handle input from file or stdin
            if not self.options.input:
                self.options.input = sys.stdin
            self.engine.translate_main()

        return self.exit_code

    def run(self, args: Optional[List[str]] = None) -> int:
        try:
            if '--no-init' not in args:
                load_init_script(self.options)

            self.options = parse_args(args)

            if self.options.info_only is not None:
                return self._handle_info_request()

            self._init_misc()
            self.init_engine()

            if self.options.interactive and not self.options.no_rlwrap:
                return run_interactive()
            elif self.options.emacs and not self.options.interactive and not self.options.no_rlwrap:
                return run_emacs_mode()
            else:
                return self.run_single()

        except KeyboardInterrupt:
            return 130
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            if self.options.debug:
                raise
            return 1

    def init_engine(self):
        if self.options.engine not in self.engines:
            raise ValueError(f'Unknown engine: {self.options.engine}')
        # Construct engine
        self.engine = self.engines[self.options.engine](self.options)


def main():
    cli = TranslationCLI()
    return cli.run(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(main())
