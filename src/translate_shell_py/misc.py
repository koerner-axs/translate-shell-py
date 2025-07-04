import re
import subprocess
from typing import List, Optional, Dict


def _get_user_lang() -> str:
    """Get user language from system (placeholder)"""
    # TODO: This would typically detect system language
    return 'en'


def _yn_to_bool(value: str) -> bool:
    """Convert Y/n string to boolean"""
    if value.lower() in ('y', 'yes', '1', 'true', 'on'):
        return True
    elif value.lower() in ('n', 'no', '0', 'false', 'off'):
        return False
    else:
        # Default to True for 'Y/n' type options
        return True


def _parse_language_codes(codes_str: str) -> List[str]:
    """Parse language codes separated by +"""
    return codes_str.split('+') if codes_str else []


def _parse_shortcut_format(arg: str) -> Optional[Dict[str, List[str]]]:
    """Parse shortcut format like 'en:es' or 'en=es+fr'"""

    # TODO: REFACTOR, WTF
    # Match patterns like 'CODE:CODE+...' or 'CODE=CODE+...'
    pattern = r'^[{(\[]?((@?[a-z]{2,3}(-[a-zA-Z]{2,4})?\+)*(@?[a-z]{2,3}(-[a-zA-Z]{2,4})?)?)?([:=])((@?[a-z]{2,3}(-[a-zA-Z]{2,4})?\+)*(@?[a-z]{2,3}(-[a-zA-Z]{2,4})?))[})\]]?$'

    match = re.match(pattern, arg)
    if match:
        source_codes = match.group(1) if match.group(1) else ''
        target_codes = match.group(7) if match.group(7) else ''

        result = {}
        if source_codes:
            result['sls'] = _parse_language_codes(source_codes)
            result['sl'] = result['sls'][0] if result['sls'] else 'auto'
        if target_codes:
            result['tl'] = _parse_language_codes(target_codes)

        return result
    return None


def detect_pager() -> Optional[str]:
    """Detect external terminal pager (less, more, most)"""
    try:
        subprocess.run(['less', '-V'], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, check=True)
        return 'less'
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(['more', '-V'], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, check=True)
            return 'more'
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run(['most'], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, check=True)
                return 'most'
            except (subprocess.CalledProcessError, FileNotFoundError):
                return None


def _has_fribidi() -> bool:
    """Check if FriBidi is available"""
    try:
        subprocess.run(['fribidi', '--version'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
