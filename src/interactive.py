import argparse

from src.translate import TranslationEngine


def print_welcome():
    pass


def prompt() -> str:
    pass


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


def is_command(user_input: str):
    return user_input.lstrip().startswith(':')


def execute_command(user_input):
    pass


def run_interactive(options: argparse.Namespace, engine: TranslationEngine) -> int:
    print_welcome()
    while True:
        user_input = prompt()
        if is_command(user_input):
            execute_command(user_input)
            continue

        translation = engine.translate(user_input)

    print("Interactive mode would be implemented here")
    return 0

def run_emacs_mode() -> int:
    print("Emacs mode would be implemented here")
    return 0
