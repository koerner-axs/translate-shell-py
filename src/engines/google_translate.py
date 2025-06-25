import argparse
import json
import urllib.parse
from typing import override

from src.langdata import get_code
from src.misc import prettify
from src.translate import TranslationEngine


class GoogleTranslateResponse:
    def __init__(self, content):
        self.translations = [x[0] for x in content[0] if x and x[0]] if content[0] else []
        self.original = [x[1] for x in content[0] if x and x[1]] if content[0] else []
        self.phonetics = [x[2] for x in content[0] if x and x[2]] if content[0] else []
        self.orig_phonetics = [x[3] for x in content[0] if x and x[3]] if content[0] else []

        # 1 - word classes and explanations
        self.words = self._parse_words(content[1]) if content[1] else {}

        # 5 - alternative translations
        self.alternatives = self._parse_alternatives(content[5]) if content[5] else {}

        # 7 - autocorrection
        if content[7] is not None and len(content[7]) >= 5:
            self.autocorrected_input = bool(content[7][5])
            self.correction_hint = content[7][1]
        else:
            self.autocorrected_input = False
            self.correction_hint = None

        # 2 & 8 - identified source languages
        self.identified_langs = []
        if content[2]:
            self.identified_langs.append(content[2])
        if content[8] and len(content[8]) >= 1 and content[0]:
            self.identified_langs.extend([x for x in content[8][0] if x])

        # 11 - (original) word classes and synonyms
        self.orig_synonyms = self._parse_orig_synonyms(content[11]) if content[11] else {}

        # 12 - (original) word classes and explanations
        self.orig_words = self._parse_orig_words(content[12]) if content[12] else {}

        # 13 - (original) examples
        self.orig_examples = self._parse_orig_examples(content[13]) if content[13] else []

        # 14 - (original) see also
        self.orig_see_also = content[14][0] if content[14] and len(content[14]) and content[14][0] else []

        # 18 - gender-specific translations
        self.gendered = self._parse_gendered(content[18]) if content[18] else []

    @staticmethod
    def _parse_words(content):
        words = {}
        for x in content:
            if x and len(x) >= 3 and x[0] and x[2]:
                inner_words = {}
                for y in x[2]:
                    if y and len(y) >= 2 and y[0] and y[1]:
                        inner_words[y[0]] = y[1]
                words[x[0]] = inner_words
        return words

    @staticmethod
    def _parse_alternatives(content):
        alternatives = {}
        for x in content:
            if x and len(x) >= 3 and x[0] and x[2]:
                alternatives[x[0]] = [y[0] for y in x[2] if y and y[0]]
        return alternatives

    @staticmethod
    def _parse_orig_synonyms(content):
        # TODO: check if this is to the API spec, I can't reproduce a case where this field is set
        orig_synonyms = {x[0]: 'whatever' for x in content[11]} if content[11] else None
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
        orig_examples = []
        if len(content) >= 1 and content[0]:
            for x in content[0]:
                if x and len(x) >= 1 and x[0]:
                    orig_examples.append(x[0])
        return orig_examples

    @staticmethod
    def _parse_gendered(content):
        gendered = {}
        if len(content) >= 1 and content[0]:
            _keys = ['male', 'female']
            for i, x in enumerate(content[0]):
                if x and len(x) >= 2 and x[1]:
                    gendered[_keys[i]] = x[1]
        return gendered


def _escape_text(text: str) -> str:
    """URL encode text for request"""
    return urllib.parse.quote(text, safe='')


def _format_phonetics(phonetics: str, lang: str) -> str:
    """Format phonetics display. Add /slashes/ for IPA phonemic notations and (parentheses) for others"""
    return f'/{phonetics}/' if lang == 'en' else f'({phonetics})'


class GoogleTranslationEngine(TranslationEngine):
    """Google Translate API implementation"""

    def __init__(self, options: argparse.Namespace):
        super().__init__(options)
        self.http_port = 80
        self.http_path_prefix = ""
        self.tk_cache = {}
        #self.options = {
        #    "no-autocorrect": False,
        #    "dump": False,
        #    "verbose": 0,
        #    "show-original": True,
        #    "show-original-phonetics": True,
        #    "show-translation": True,
        #    "show-translation-phonetics": True,
        #    "show-prompt-message": True,
        #    "show-languages": True,
        #    "show-original-dictionary": True,
        #    "show-dictionary": True,
        #    "show-alternatives": True,
        #    "fmt-languages": "[ %s -> %t ]"
        #}

    @override
    def initialize(self):
        """Initialize the Google Translate engine"""
        pass # nothing to do

    def request_url(self, text: str, sl: str, tl: str, hl: str) -> str:
        """Generate request URL for Google Translate"""
        qc = "qc" if self.options.no_autocorrect else "qca"

        return (f"http://translate.googleapis.com/translate_a/single?client=gtx"
                f"&ie=UTF-8&oe=UTF-8"
                f"&dt=bd&dt=ex&dt=ld&dt=md&dt=rw&dt=rm&dt=ss&dt=t&dt=at&dt=gt"
                f"&dt={qc}&sl={sl}&tl={tl}&hl={hl}"
                f"&q={_escape_text(text)}")

    @override
    def post_request_url(self, text: str, sl: str, tl: str, hl: str, req_type: str) -> str:
        """Generate POST request URL"""
        # Google Translate typically uses GET requests
        return self.request_url(text, sl, tl, hl)

    @override
    def post_request_content_type(self, text: str, sl: str, tl: str, hl: str, req_type: str) -> str:
        """Get POST request content type"""
        return 'application/x-www-form-urlencoded'

    @override
    def post_request_user_agent(self, text: str, sl: str, tl: str, hl: str, req_type: str) -> str:
        """Get POST request user agent"""
        return 'Mozilla/5.0 (compatible; GoogleTranslate)'

    @override
    def post_request_body(self, text: str, sl: str, tl: str, hl: str, req_type: str) -> str:
        """Generate POST request body"""
        return '' # Google Translate uses GET requests typically

    @override
    def tts_url(self, text: str, tl: str) -> str:
        """Generate text-to-speech URL"""
        return (f"https://{self.http_host}/translate_tts?ie=UTF-8&client=gtx"
                f"&tl={tl}&q={_escape_text(text)}")

    @override
    def web_translate_url(self, uri: str, sl: str, tl: str, hl: str) -> str:
        """Generate web translation URL"""
        return (f"https://translate.google.com/translate?"
                f"hl={hl}&sl={sl}&tl={tl}&u={uri}")

    @override
    def _translate(self, text: str, source_lang: str, target_lang: str, host_lang: str
                   , is_verbose: bool = False
                   #, to_speech: bool = False
                   #, return_playlist: Optional[List] = None
                   #, return_il: Optional[List] = None
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

        # Get response from Google Translate
        url = self.request_url(text, code_source_lang, code_target_lang, code_host_lang)
        content = self.http_get(url)

        if self.options.dump:
            return content

        content = json.loads(content)
        if not content:
            return "[ERROR] Could not parse translation response"

        response = GoogleTranslateResponse(content)




        #translation = " ".join(translations) if translations else ""


        # Set identified language
        #if return_il is not None:
        #    il = source_lang if not ils or source_lang in ils else ils[0]
        #    return_il.append(il)
        #    if self.options.verbose < -1:
        #        return il
        #    elif self.options.verbose < 0:
        #        return self._get_language(il)

        if is_verbose:
            return self.format_verbose(response)
        else:
            return self.format_brief(response, is_phonetic)

    def format_verbose(self, response) -> str:
        """Format engine response verbosely"""
        result_parts = []

        # Show original text
        if self.options.show_original and len(response.original) > 0:
            result_parts.append("Original:")
            result_parts.append(prettify("original", " ".join(response.original)))
            if self.options.show_original_phonetics and len(response.orig_phonetics) > 0:
                # TODO: check this holds, maybe refactor to reduce implicit knowledge
                identified_source_lang = response.identified_langs[0]
                result_parts.append(_format_phonetics(" ".join(response.orig_phonetics), identified_source_lang))

        # Show translation
        if self.options.show_translation:
            result_parts.append("Translation:")
            if len(response.gendered) > 0:
                # TODO: check if the wrong way around
                result_parts.append(f"(♂) {response.gendered.get('male', '')}")
                result_parts.append(f"(♀) {response.gendered.get('female', '')}")
            else:
                result_parts.append(prettify("translation", translation))

            if self.options.show_translation_phonetics and phonetics:
                result_parts.append(_format_phonetics(" ".join(phonetics), target_lang))

        # Show language direction
        if self.options.show_languages:
            lang_format = self.options.fmt_languages
            lang_display = lang_format.replace("%s", self._get_display(source_lang))
            lang_display = lang_display.replace("%t", self._get_display(target_lang))
            result_parts.append(lang_display)

        if to_speech and return_playlist is not None:
            return_playlist.extend([
                {"text": " ".join(original), "tl": source_lang},
                {"text": self._show_translations_of(host_lang, ""), "tl": code_host_lang},
                {"text": translation, "tl": code_target_lang}
            ])

        return "\n".join(result_parts)

    def format_brief(self, response, is_phonetic: bool) -> str:
        """Format engine response briefly"""

        if is_phonetic and len(response.phonetics) > 0:
            result = prettify("brief-translation-phonetics", " ".join(response.phonetics))
        elif len(response.translations) > 0:
            result = prettify("brief-translation", " ".join(response.translation))
        else:
            result = prettify("error", "Brief formatting failed, engine response likely invalid - rare error")

        # TODO: implement these features or remove
        # if to_speech and return_playlist is not None:
        #    return_playlist.append({
        #        "text": translation,
        #        "tl": code_target_lang
        #    })

        return result










    def _get_language(self, code: str) -> str:
        """Get language name from code"""
        # This would normally map codes to language names
        return code

    def _get_display(self, code: str) -> str:
        """Get display name for language"""
        return self._get_language(code)

    def _get_name(self, code: str) -> str:
        """Get name for language"""
        return self._get_language(code)

    def _show_definitions_of(self, hl: str, word: str) -> str:
        """Get 'Definitions of' text in host language"""
        return f"Definitions of {word}"

    def _show_translations_of(self, hl: str, word: str) -> str:
        """Get 'Translations of' text in host language"""
        return f"Translations of {word}"

    def _show_synonyms(self, hl: str) -> str:
        """Get 'Synonyms' text in host language"""
        return "Synonyms"

    def _show_examples(self, hl: str) -> str:
        """Get 'Examples' text in host language"""
        return "Examples"

    def _show_see_also(self, hl: str) -> str:
        """Get 'See also' text in host language"""
        return "See also"
