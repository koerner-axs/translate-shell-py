from termcolor import colored


STYLES = {
    'unstyled': lambda text: colored(f'unstyled: {text}', color='magenta', attrs=['strike']),
    'basic': lambda text: text,
    'debug': lambda text: colored(f'-- {text}', color='cyan'),

    'information-key': lambda text: text,
    'information-value': lambda text: colored(text, attrs=['bold']),

    'translation': lambda text: colored(text, attrs=['bold']),
    'translation-phonetics': lambda text: colored(text, attrs=['bold']),
    'prompt-message-original': lambda text: colored(text, attrs=['underline']),
    'languages-source': lambda text: colored(text, attrs=['underline']),
    'languages-target': lambda text: colored(text, attrs=['bold']),
    'dictionary-word': lambda text: colored(text, attrs=['bold']),
    'alternatives-original': lambda text: colored(text, attrs=['underline']),
    'alternatives-translations-item': lambda text: colored(text, attrs=['bold']),
}
# TODO: transfer from AWK to style dict
#     Option["sgr-original-dictionary-detailed-explanation"] = "bold"
#     Option["sgr-original-dictionary-detailed-synonyms-item"] = "bold"
#     Option["sgr-original-dictionary-synonyms-synonyms-item"] = "bold"
#     Option["sgr-original-dictionary-examples-original"][1] = "bold"
#     Option["sgr-original-dictionary-examples-original"][2] = "underline"
#     Option["sgr-original-dictionary-see-also-phrases-item"] = "bold"
#     Option["fmt-welcome-message"] = Name
#     Option["sgr-welcome-message"] = "bold"
#     Option["fmt-welcome-submessage"] = "(:q to quit)"
#     Option["fmt-prompt"] = "%s> "
#     Option["sgr-prompt"] = "bold"

# TODO: Replace when a theme system is implemented
STYLES['brief-translation'] = STYLES['basic']
STYLES['brief-translation-phonetics'] = STYLES['basic']
STYLES['original'] = STYLES['basic']
STYLES['original-phonetics'] = STYLES['basic']
STYLES['prompt-message'] = STYLES['basic']
STYLES['languages'] = STYLES['basic']
STYLES['dictionary-word-class'] = STYLES['basic']
STYLES['dictionary-explanations-item'] = STYLES['basic']


def prettify(style: str, text: str) -> str:
    """Apply styling to text"""
    if style not in STYLES:
        return STYLES['unstyled'](text)
    return STYLES[style](text)
