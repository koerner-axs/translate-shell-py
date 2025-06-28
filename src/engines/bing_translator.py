import argparse
import json
import re
from dataclasses import dataclass
from typing import override, List, Optional

from src.langdata import get_code
from src.misc import prettify
from src.translate import TranslationEngine, _escape_text


def first_match(pattern: str, data: str) -> re.Match | None:
    for match in re.finditer(pattern, data):
        return match
    return None


@dataclass
class BingAccessToken:
    ig: str
    iid: str
    session_start: int
    token: str
    valid_for_millis: int

    @staticmethod
    def from_token_request_response(content: str) -> "BingAccessToken":
        if (match := first_match('IG:"([^"]+)"', content)) and (data := match.group(1)) and len(data) == 32:
            ig = data
        else:
            raise RuntimeError('Could not parse required session token field from Bing response: IG')

        # Typically matches 4 strings, just take the first one
        if ((match := first_match('data-iid="([^"]+)"', content))
                and (data := match.group(1)) and len(data) == 15):
            iid = data
        else:
            raise RuntimeError('Could not parse required session token field from Bing response: IID')

        # Typically matches exactly once
        if ((match := first_match('params_AbusePreventionHelper = ([^;]+);', content))
                and (data := match.group(1))
                and (obj := json.loads(data)) and len(obj) == 3):
            session_start, token, valid_for_millis = obj
        else:
            raise RuntimeError('Could not parse required session token field from Bing response: Token')

        return BingAccessToken(ig, iid, session_start, token, valid_for_millis)


class BingTranslatorResponse:
    def __init__(self, content):
        self.identified_lang = content[0]['detectedLanguage']['language']
        # TODO: do not print phonetics if equal to translation (redundant)
        self.translations = self._parse_translations(content)

    @staticmethod
    def _parse_translations(content):
        if len(content) < 1 or not content[0] or 'translations' not in content[0]:
            return []
        content = content[0]['translations']

        translations = []
        for x in content:
            if 'text' in x:
                translation = {'text': x['text']}
                if ('transliteration' in x and (transl_dict := x['transliteration']) and 'text' in transl_dict
                    and (transliteration := transl_dict['text'])) and transliteration:
                    translation['transliteration'] = transliteration
                translations.append(translation)
        return translations


# See BingTranslator.awk::225ff.
MAP = {
    'auto': 'auto-detect',
    'tl': 'fil',  # Bing code for Filipino
    'hmn': 'mww',  # Bing code for Hmong Daw
    'ku': 'kmr',  # Bing code for Northern Kurdish
    'ckb': 'ku',  # Bing code for Central Kurdish
    'mn': 'mn-Cyrl',  # Bing code for Mongolian (Cyrillic)
    'no': 'nb',  # Bing code for Norwegian Bokmål
    'pt-BR': 'pt',  # Bing code for Brazilian Portuguese
    'pt-PT': 'pt-pt',  # Bing code for European Portuguese
    'zh-CN': 'zh-Hans',
    'zh-TW': 'zh-Hant',
}

def _map_to_bing_lang_code(code: str) -> str:
    return MAP[code] if code in MAP else code


class BingTranslatorEngine(TranslationEngine):
    """Google Translate API implementation"""

    def __init__(self, options: argparse.Namespace):
        super().__init__(options)
        self.access_token: BingAccessToken | None = None

    @override
    def initialize(self):
        """Initialize the Bing Translator engine"""
        content = self.http_get(self.get_endpoint('gettoken'))
        self.access_token = BingAccessToken.from_token_request_response(content)

    def get_endpoint(self, name: str) -> str:
        """Generate request URL for Bing Translator"""
        if name == 'gettoken':
            return 'http://bing.com/translator'
        elif name == 'lookup':
            return 'http://bing.com/tlookupv3'
        elif name == 'translate':
            return f'http://www.bing.com/ttranslatev3?IG={self.access_token.ig}&IID={self.access_token.iid}'
        else:
            raise ValueError(f'Unknown endpoint: {name}')

    def request_body(self, text: str, sl: str, tl: str, name: str) -> str:
        """Generate request body for Bing Translator"""
        if name == 'lookup':
            return f'&text={_escape_text(text)}&from={sl}&to={tl}'
        elif name == 'translate':
            return (f'&text={_escape_text(text)}&fromLang={sl}&to={tl}'
                    f'&token={_escape_text(self.access_token.token)}&key={self.access_token.session_start}')
        else:
            raise ValueError(f'Unknown request type: {name}')

    @override
    def tts_url(self, text: str, tl: str):
        """Generate text-to-speech URL - to be implemented by specific engines"""
        pass

    @override
    def web_translate_url(self, uri: str, sl: str, tl: str, hl: str) -> str:
        """Generate web translation URL - to be implemented by specific engines"""
        pass

    @override
    def _translate(self, text: str, source_lang: str, target_lang: str, host_lang: str
                   , is_verbose: bool
                   # TODO: implement these features or remove
                   #, to_speech: bool
                   #, return_playlist: Optional[List]
                   #, return_il: Optional[List]
                   ) -> str:
        """Core translation function"""

        # Check if target language is phonetic
        is_phonetic = target_lang.startswith('@')
        if is_phonetic:
            target_lang = target_lang[1:]

        # Convert language codes
        code_source_lang = get_code(source_lang) or source_lang
        code_target_lang = get_code(target_lang) or target_lang
        code_host_lang = get_code(host_lang) or host_lang
        bing_code_source_lang = _map_to_bing_lang_code(code_source_lang)
        bing_code_target_lang = _map_to_bing_lang_code(code_target_lang)

        # Get response from Bing Translator
        url = self.get_endpoint('translate')
        content = self.http_post(url, self.request_body(text, bing_code_source_lang, bing_code_target_lang, 'translate'),
                                 content_type='application/x-www-form-urlencoded')

        # TODO: Bing seems not to realize which target language is requested. Check params!!

        if self.options.dump:
            return content

        content = json.loads(content)
        if not content:
            return '[ERROR] Could not parse json response'

        response = BingTranslatorResponse(content)

        # TODO: Show Transliteration

        if is_verbose:
            return self.format_verbose(response)
        else:
            return self.format_brief(response, is_phonetic, code_target_lang)

    def format_verbose(self, response: BingTranslatorResponse):
        """Format engine response verbosely"""
        result_parts = []
        pass

    def format_brief(self, response: BingTranslatorResponse, is_phonetic: bool, code_target_lang: str) -> str:
        """Format engine response briefly"""

        if len(response.translations) == 0:
            return prettify('error', 'Brief formatting failed, engine response likely invalid - rare error')

        translation, transliteration = response.translations[0]['text'], response.translations[0].get('transliteration')
        if is_phonetic and transliteration and translation != transliteration:
            result = prettify('brief-translation-phonetics', transliteration)
        else:
            result = prettify('brief-translation', translation)

        # TODO: implement these features or remove
        # TODO: warning: code_target_lang is not the bing language code
        # if to_speech and return_playlist is not None:
        #    return_playlist.append({
        #        "text": translation,
        #        "tl": code_target_lang
        #    })

        return result
