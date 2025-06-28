import argparse
import json
from dataclasses import dataclass
from typing import override, List

from src.langdata import get_code, get_endonym, show_definitions_of, show_translations_of
from src.theme import prettify
from src.translate import TranslationEngine, _escape_text, format_phonetics


@dataclass
class DictionaryEntry:
    word: str
    article: str
    back_translations: List[str]


class GoogleTranslateResponse:
    def __init__(self, content):
        self.translations = self._parse_translations(content)
        self.originals = self._parse_originals(content)
        self.phonetics = self._parse_phonetics(content)
        self.orig_phonetics = self._parse_orig_phonetics(content)

        self.dictionary = self._parse_dictionary(content)
        self.alternatives = self._parse_alternatives(content)

        # 7 - autocorrection
        if content[7] is not None and len(content[7]) >= 5:
            self.autocorrected_input = bool(content[7][5])
            self.correction_hint = content[7][1]
        else:
            self.autocorrected_input = False
            self.correction_hint = None

        self.identified_langs = self._parse_identified_langs(content)
        self.orig_synonyms = self._parse_orig_synonyms(content)
        self.orig_words = self._parse_orig_words(content)
        self.orig_examples = self._parse_orig_examples(content)
        self.orig_see_also = self._parse_orig_see_also(content)
        self.gendered = self._parse_gendered(content)

    @staticmethod
    def _parse_translations(content):
        if len(content) < 1 or not content[0]:
            return []
        content = content[0]

        translations = []
        for x in content:
            if x and len(x) >= 1 and x[0]:
                translations.append(x[0])
        return translations

    @staticmethod
    def _parse_originals(content):
        if len(content) < 1 or not content[0]:
            return []
        content = content[0]

        originals = []
        for x in content:
            if x and len(x) >= 2 and x[1]:
                originals.append(x[1])
        return originals

    @staticmethod
    def _parse_phonetics(content):
        if len(content) < 1 or not content[0]:
            return []
        content = content[0]

        phonetics = []
        for x in content:
            if x and len(x) >= 3 and x[2]:
                phonetics.append(x[2])
        return phonetics

    @staticmethod
    def _parse_orig_phonetics(content):
        if len(content) < 1 or not content[0]:
            return []
        content = content[0]

        orig_phonetics = []
        for x in content:
            if x and len(x) >= 4 and x[3]:
                orig_phonetics.append(x[3])
        return orig_phonetics

    @staticmethod
    def _parse_dictionary(content):
        if len(content) < 2 or not content[1]:
            return {}
        content = content[1]

        dictionary = {}
        for x in content:
            if x and len(x) >= 3 and x[0] and x[2]:
                word_class, entries = x[0], x[2]
                entries_for_class = []
                for y in entries:
                    word, back_translations, article = y[0], y[1], y[4]
                    if y and len(y) >= 2 and y[0] and y[1]:
                        entries_for_class.append(DictionaryEntry(word, article, back_translations))
                dictionary[word_class] = entries_for_class
        return dictionary

    @staticmethod
    def _parse_alternatives(content):
        if len(content) < 6 or not content[5]:
            return {}
        content = content[5]

        alternatives = {}
        for x in content:
            if x and len(x) >= 3 and x[0] and x[2]:
                alternatives[x[0]] = [y[0] for y in x[2] if y and y[0]]
        return alternatives

    @staticmethod
    def _parse_identified_langs(content):
        identified_langs = []
        if len(content) >= 3 and content[2]:
            identified_langs.append(content[2])
        if len(content) >= 9 and content[8] and len(content[8]) >= 1 and content[8][0]:
            identified_langs.extend([x for x in content[8][0] if x])
        return identified_langs

    @staticmethod
    def _parse_orig_synonyms(content):
        if len(content) < 12 or not content[11]:
            return {}
        content = content[11]

        # TODO: check if this is to the API spec, I can't reproduce a case where this field is set
        orig_synonyms = {x[0]: 'whatever' for x in content} if content else None
        # TODO: here I stopped, didn't know how to make sense of this monstrosity
        #       The two refs are somehow used to 2D index into oSynonyms, but no clue what they represent

        #   if (match(i, "^0" SUBSEP "11" SUBSEP "([[:digit:]]+)" SUBSEP "0$", group))
        #       oSynonymClasses[group[1]] = literal(json[i])
        #   if (match(i, "^0" SUBSEP "11" SUBSEP "([[:digit:]]+)" SUBSEP "1" SUBSEP "([[:digit:]]+)" SUBSEP "1$", group))
        #       if (json[i]) {
        #           oRefs[literal(json[i])][1] = group[1]
        #           oRefs[literal(json[i])][2] = group[2]
        #       }
        #   if (match(i, "^0" SUBSEP "11" SUBSEP "([[:digit:]]+)" SUBSEP "1" SUBSEP "([[:digit:]]+)" SUBSEP "0" SUBSEP "([[:digit:]]+)$", group))
        #       oSynonyms[group[1]][group[2]][group[3]] = literal(json[i])
        return orig_synonyms

    @staticmethod
    def _parse_orig_words(content):
        if len(content) < 13 or not content[12]:
            return {}
        content = content[12]

        orig_words = {}
        for x in content:
            if x and len(x) >= 2 and x[0] and x[1]:
                inner_list = []
                for y in x[1]:
                    if y and len(y) >= 1:
                        inner_dict = {}
                        _keys = ['explanation', 'ref', 'example']
                        for i, z in enumerate(y[:3]):
                            if z:
                                inner_dict[_keys[i]] = z
                        if len(inner_dict) >= 1:
                            inner_list.append(inner_dict)
                orig_words[x[0]] = inner_list
        return orig_words

    @staticmethod
    def _parse_orig_examples(content):
        if len(content) < 14 or not content[13]:
            return []
        content = content[13]

        orig_examples = []
        if len(content) >= 1 and content[0]:
            for x in content[0]:
                if x and len(x) >= 1 and x[0]:
                    orig_examples.append(x[0])
        return orig_examples

    @staticmethod
    def _parse_orig_see_also(content):
        if len(content) < 15 or not content[14]:
            return []
        content = content[14]

        return content[0] if len(content) > 0 and content[0] else []

    @staticmethod
    def _parse_gendered(content):
        if len(content) < 19 or not content[18]:
            return []
        content = content[18]

        gendered = {}
        if len(content) >= 1 and content[0]:
            _keys = ['male', 'female']
            for i, x in enumerate(content[0]):
                if x and len(x) >= 2 and x[1]:
                    gendered[_keys[i]] = x[1]
        return gendered


class GoogleTranslationEngine(TranslationEngine):
    """Google Translate API implementation"""

    def __init__(self, options: argparse.Namespace):
        super().__init__(options)

    @override
    def initialize(self):
        """Initialize the Google Translate engine"""
        pass # nothing to do

    def request_url(self, text: str, sl: str, tl: str, hl: str) -> str:
        """Generate request URL for Google Translate"""
        qc = 'qc' if self.options.no_autocorrect else 'qca'

        return (f'http://translate.googleapis.com/translate_a/single?client=gtx'
                f'&ie=UTF-8&oe=UTF-8'
                f'&dt=bd&dt=ex&dt=ld&dt=md&dt=rw&dt=rm&dt=ss&dt=t&dt=at&dt=gt'
                f'&dt={qc}&sl={sl}&tl={tl}&hl={hl}'
                f'&q={_escape_text(text)}')

    @override
    def tts_url(self, text: str, tl: str) -> str:
        """Generate text-to-speech URL"""
        return (f'https://{None}/translate_tts?ie=UTF-8&client=gtx'
                f'&tl={tl}&q={_escape_text(text)}')

    @override
    def web_translate_url(self, uri: str, sl: str, tl: str, hl: str) -> str:
        """Generate web translation URL"""
        return (f'https://translate.google.com/translate?'
                f'hl={hl}&sl={sl}&tl={tl}&u={uri}')

    @override
    def _translate(self, text: str, source_lang: str, target_lang: str, host_lang: str
                   , is_verbose: bool = False
                   #, to_speech: bool = False
                   #, return_playlist: Optional[List] = None
                   #, return_il: Optional[List] = None
                   ) -> (str, str):
        """Core translation function"""

        # Check if target language is phonetic
        is_phonetic = target_lang.startswith('@')
        if is_phonetic:
            target_lang = target_lang[1:]

        # Convert language codes
        code_source_lang = get_code(source_lang) or source_lang
        code_target_lang = get_code(target_lang) or target_lang
        code_host_lang = get_code(host_lang) or host_lang

        # Get response from Google Translate
        url = self.request_url(text, code_source_lang, code_target_lang, code_host_lang)
        content = self.http_get(url)

        if self.options.dump:
            return content

        content = json.loads(content)
        response = GoogleTranslateResponse(content)

        # Set identified language
        # TODO: check this holds, maybe refactor to reduce implicit knowledge, referring to identified_langs
        if code_source_lang == 'auto' and len(response.identified_langs) >= 1:
            code_source_lang = response.identified_langs[0]
        if not code_target_lang and len(response.identified_langs) >= 2:
            code_target_lang = response.identified_langs[1]

        if is_verbose:
            output = self.format_verbose(response, code_host_lang, code_source_lang, code_target_lang)
        else:
            output = self.format_brief(response, is_phonetic, code_target_lang)

        return output, code_source_lang

    def format_verbose(self, response: GoogleTranslateResponse, code_host_lang, code_source_lang, code_target_lang) -> str:
        """Format engine response verbosely"""
        result_parts = []

        # Show original text
        if self.options.show_original and len(response.originals) > 0:
            self.if_debug(result_parts, 'display original text & phonetics')
            result_parts.append(prettify('original', ' '.join(response.originals)))
            if self.options.show_original_phonetics and len(response.orig_phonetics) > 0:
                result_parts.append(prettify('original-phonetics',
                                             format_phonetics(' '.join(response.orig_phonetics), code_source_lang)))

        # Show translation
        if self.options.show_translation:
            result_parts.append('')
            self.if_debug(result_parts, 'display major translation & phonetics')
            if len(response.gendered) > 0:
                # TODO: check if the wrong way around (error in parsing)
                result_parts.append(prettify('prompt-message', '(♂) ') +
                                    prettify('translation', response.gendered.get('male', '')))
                result_parts.append(prettify('prompt-message', '(♀) ') +
                                    prettify('translation', response.gendered.get('female', '')))
            else:
                result_parts.append(prettify('translation', ' '.join(response.translations)))
            if self.options.show_translation_phonetics and response.phonetics:
                result_parts.append(prettify('translation-phonetics',
                                             format_phonetics(' '.join(response.phonetics), code_target_lang)))

        if self.options.show_prompt_message or self.options.show_languages:
            result_parts.append('')

        # Show prompt
        if self.options.show_prompt_message:
            self.if_debug(result_parts, 'display prompt message')
            prompt_template = None
            if len(response.dictionary) > 0:
                prompt_template = show_definitions_of(code_host_lang)
            elif len(response.alternatives) > 0:
                prompt_template = show_translations_of(code_host_lang)
            if prompt_template:
                # TODO: missing RTL support
                prompt = prompt_template % prettify('prompt-message-original', ' '.join(response.originals))
                result_parts.append(prettify('prompt-message', prompt))

        # Show language direction
        if self.options.show_languages:
            self.if_debug(result_parts, 'display source language -> target language')
            result_parts.append(prettify('languages', '[ ') +
                                prettify('languages-source', get_endonym(code_source_lang)) +
                                prettify('languages', ' -> ') +
                                prettify('languages-target', get_endonym(code_target_lang)) +
                                prettify('languages', ' ]'))

        # TODO: Show original dictionary
        self.if_debug(result_parts, 'display original dictionary entries')

        # Show dictionary
        result_parts.append('')
        self.if_debug(result_parts, 'display dictionary entries')
        for word_class, dictionary in response.dictionary.items():
            result_parts.append(prettify('dictionary-word-class', word_class))
            for entry in dictionary:
                # TODO: missing RTL support
                word = f'({entry.article}) {entry.word}' if entry.article else entry.word
                result_parts.append(self.indent(1, prettify('dictionary-word', word)))
                pretty_back_translations = [prettify('dictionary-explanations-item', x) for x in entry.back_translations]
                result_parts.append(self.indent(2, prettify('basic', ', ').join(pretty_back_translations)))

        # Show alternative translations
        result_parts.append('')
        self.if_debug(result_parts, 'display alternative translations')
        for original, translations in response.alternatives.items():
            result_parts.append(prettify('alternatives-original', original))
            # TODO: missing RTL support, or am I? I feel like the translation should be adjusted to the host lang or src
            pretty_translations = [prettify('alternatives-translations-item', x) for x in translations]
            result_parts.append(self.indent(1, prettify('basic', ', ').join(pretty_translations)))

        # TODO: implement these features or remove
        #if to_speech and return_playlist is not None:
        #    return_playlist.extend([
        #        {'text': ' '.join(original), 'tl': source_lang},
        #        {'text': self._show_translations_of(host_lang, ''), 'tl': code_host_lang},
        #        {'text': translation, 'tl': code_target_lang}
        #    ])

        return '\n'.join(result_parts)

    @staticmethod
    def format_brief(response: GoogleTranslateResponse, is_phonetic: bool, code_target_lang: str) -> str:
        """Format engine response briefly"""

        if is_phonetic and len(response.phonetics) > 0:
            result = prettify('brief-translation-phonetics', ' '.join(response.phonetics))
        elif len(response.translations) > 0:
            result = prettify('brief-translation', ' '.join(response.translations))
        else:
            result = prettify('error', 'Brief formatting failed, engine response likely invalid - rare error')

        # TODO: implement these features or remove
        # if to_speech and return_playlist is not None:
        #    return_playlist.append({
        #        'text': translation,
        #        'tl': code_target_lang
        #    })

        return result
