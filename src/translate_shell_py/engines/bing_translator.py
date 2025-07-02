import argparse
import json
import re
from dataclasses import dataclass
from typing import override

from ..langdata import get_code, get_endonym
from ..theme import prettify
from ..translate import TranslationEngine, _escape_text, format_phonetics, Translation


def first_match(pattern: str, data: str) -> re.Match | None:
    return re.compile(pattern).search(data)


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
        self.translation = self._parse_translation(content)
        self.orig_phonetics = None

    def ingest_original_phonetics_response(self, content):
        # If the display of original phonetics is requested, additional data is queried and ingested here
        translation = self._parse_translation(content)
        if translation:
            self.orig_phonetics = translation.get('transliteration')

    @staticmethod
    def _parse_translation(content):
        if len(content) < 1 or not content[0] or 'translations' not in content[0]:
            return []
        content = content[0]['translations']

        if len(content) >= 1:
            if 'text' in content[0]:
                translation = {'text': content[0]['text']}
                if ('transliteration' in content[0] and (transl_dict := content[0]['transliteration'])
                    and 'text' in transl_dict and (transliteration := transl_dict['text']) and transliteration):
                    translation['transliteration'] = transliteration
                return translation
        return None


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


def _map_from_bing_lang_code(bing_code: str) -> str:
    for ours, theirs in MAP.items():
        if bing_code == theirs:
            return ours
    return bing_code


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
            return 'http://www.bing.com/translator'
        elif name == 'translate':
            return f'http://www.bing.com/ttranslatev3?IG={self.access_token.ig}&IID={self.access_token.iid}'
        else:
            raise ValueError(f'Unknown endpoint: {name}')

    def request_params(self, text: str, sl: str, tl: str) -> str:
        """Generate request body for Bing Translator"""
        return (f'&text={_escape_text(text)}&fromLang={sl}&to={tl}'
                f'&token={_escape_text(self.access_token.token)}&key={self.access_token.session_start}')

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
                   ) -> Translation:
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
        content = self.http_post(self.get_endpoint('translate'),
                                 self.request_params(text, bing_code_source_lang, bing_code_target_lang),
                                 content_type='application/x-www-form-urlencoded')
        if self.options.dump:
            return Translation(content, '', code_target_lang, [])

        content = json.loads(content)
        response = BingTranslatorResponse(content)

        # Perform additional requests
        if self.options.show_original_phonetics:
            content = self.http_post(self.get_endpoint('translate'),
                                     self.request_params(text, response.identified_lang, response.identified_lang),
                                     content_type='application/x-www-form-urlencoded')
            content = json.loads(content)
            response.ingest_original_phonetics_response(content)

        # Update source language
        if code_source_lang == 'auto' and response.identified_lang:
            code_source_lang = _map_from_bing_lang_code(response.identified_lang)

        if is_verbose:
            output = self.format_verbose(response, text, code_host_lang, code_source_lang, code_target_lang)
        else:
            output = self.format_brief(response, is_phonetic, code_target_lang)

        return Translation(output, code_source_lang, code_target_lang, audio_fragments)

    def format_verbose(self, response: BingTranslatorResponse, text_input: str, code_host_lang: str,
                       code_source_lang: str, code_target_lang: str) -> str:
        """Format engine response verbosely"""
        result_parts = []

        # Show original text
        if self.options.show_original:
            self.if_debug(result_parts, 'display original text & phonetics')
            result_parts.append(prettify('original', text_input))
            if (self.options.show_original_phonetics and response.orig_phonetics
                    and response.orig_phonetics != text_input):
                result_parts.append(prettify('original-phonetics',
                                             format_phonetics(response.orig_phonetics, code_source_lang)))

        # Show translation
        if self.options.show_translation:
            result_parts.append('')
            self.if_debug(result_parts, 'display major translation & phonetics')
            result_parts.append(prettify('translation', response.translation['text']))
            if self.options.show_translation_phonetics and 'transliteration' in response.translation:
                result_parts.append(prettify('translation-phonetics',
                                             format_phonetics(response.translation['transliteration'],
                                                              code_target_lang)))

        # Show language direction
        if self.options.show_languages:
            result_parts.append('')
            self.if_debug(result_parts, 'display source language -> target language')
            result_parts.append(prettify('languages', '[ ') +
                                prettify('languages-source', get_endonym(code_source_lang)) +
                                prettify('languages', ' -> ') +
                                prettify('languages-target', get_endonym(code_target_lang)) +
                                prettify('languages', ' ]'))

        # Show Dictionary not implemented. Bing Dict API will be shut down in August 2025.

        return '\n'.join(result_parts)

    @staticmethod
    def format_brief(response: BingTranslatorResponse, is_phonetic: bool, code_target_lang: str) -> str:
        """Format engine response briefly"""

        if not response.translation:
            return prettify('error', 'Brief formatting failed, engine response likely invalid - rare error')

        translation, transliteration = response.translation['text'], response.translation.get('transliteration')
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
