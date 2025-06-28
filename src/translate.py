import abc
import argparse
import os
import re
import subprocess
import sys
import urllib
from dataclasses import dataclass
from gettext import translation
from typing import List, Tuple
from urllib.parse import quote

import requests
from requests.auth import HTTPBasicAuth

from src.audio import play_remote_audio
from src.langdata import get_code, is_rtl, get_name
from src.misc import _has_fribidi
from src.theme import prettify


def _escape_text(text: str) -> str:
    """URL encode text for request"""
    return urllib.parse.quote(text, safe='')


def _error(message: str) -> None:
    """Print error message"""
    print(message, file=sys.stderr)


def _warning(message: str) -> None:
    """Print warning message"""
    print(message, file=sys.stderr)


def format_phonetics(phonetics: str, lang: str) -> str:
    """Format phonetics display. Add /slashes/ for IPA phonemic notations and (parentheses) for others"""
    return f'/{phonetics}/' if lang == 'en' else f'({phonetics})'


@dataclass
class Translation:
    tty_output: str
    identified_lang: str
    audio_fragments: List[Tuple[str, str]]


class TranslationEngine(metaclass=abc.ABCMeta):
    """Main translation engine class"""

    def __init__(self, options: argparse.Namespace):
        self.options: argparse.Namespace = options
        self.http_auth_user = ''
        self.http_auth_pass = ''
        self.cookie = ''
        self.pager = ''

    def http_get(self, url: str) -> str:
        """Send an HTTP GET request and get response from online translator"""

        # Prepare headers
        headers = {
            'Connection': 'close'
        }
        if self.options.user_agent:
            headers['User-Agent'] = self.options.user_agent

        # Prepare authentication
        auth = None
        if self.http_auth_user and self.http_auth_pass:
            auth = HTTPBasicAuth(self.http_auth_user, self.http_auth_pass)

        # Prepare cookies
        cookies = {}
        if self.cookie:
            # Parse cookie string into dict if needed
            if isinstance(self.cookie, str):
                for cookie_pair in self.cookie.split(';'):
                    if '=' in cookie_pair:
                        key, value = cookie_pair.strip().split('=', 1)
                        cookies[key] = value
            else:
                cookies = self.cookie

        try:
            response = requests.get(
                url,
                headers=headers,
                cookies=cookies,
                auth=auth,
                timeout=30,
                allow_redirects=True  # Handle redirects automatically
            )

            if response.status_code == 429:
                _error(
                    f'[ERROR] {self.options.engine.title()} did not return results because rate limiting is in effect')
                return ''

            # Raise an exception for HTTP error status codes (4xx, 5xx)
            response.raise_for_status()

            return response.text

        except requests.exceptions.Timeout:
            _warning('[WARNING] Request timed out')
            return ''
        except requests.exceptions.ConnectionError as e:
            _warning(f'[WARNING] Connection error: {e}')
            return ''
        except requests.exceptions.HTTPError:
            _error(
                f'[ERROR] {self.options.engine.title()} returned an error response. HTTP status code: {response.status_code}')
            return ''
        except requests.exceptions.RequestException as e:
            _warning(f'[WARNING] Request error: {e}')
            return ''

    def http_post(self, url: str, content: str, content_type: str = None) -> str:
        """Send an HTTP POST request and return response from online translator"""

        # Prepare headers
        headers = {
            'Connection': 'close'
        }
        if content_type:
            headers['Content-Type'] = content_type
        if self.options.user_agent:
            headers['User-Agent'] = self.options.user_agent

        # Prepare authentication
        auth = None
        if self.http_auth_user and self.http_auth_pass:
            auth = HTTPBasicAuth(self.http_auth_user, self.http_auth_pass)

        # Prepare cookies
        cookies = {}
        if self.cookie:
            # Parse cookie string into dict if needed
            if isinstance(self.cookie, str):
                for cookie_pair in self.cookie.split(';'):
                    if '=' in cookie_pair:
                        key, value = cookie_pair.strip().split('=', 1)
                        cookies[key] = value
            else:
                cookies = self.cookie

        try:
            response = requests.post(
                url,
                content,
                headers=headers,
                cookies=cookies,
                auth=auth,
                timeout=30,
                allow_redirects=True  # Handle redirects automatically
            )

            if response.status_code == 429:
                _error(
                    f'[ERROR] {self.options.engine.title()} did not return results because rate limiting is in effect')
                return ''

            # Raise an exception for HTTP error status codes (4xx, 5xx)
            response.raise_for_status()

            return response.text

        except requests.exceptions.Timeout:
            _warning('[WARNING] Request timed out')
            return ''
        except requests.exceptions.ConnectionError as e:
            _warning(f'[WARNING] Connection error: {e}')
            return ''
        except requests.exceptions.HTTPError:
            _error(
                f'[ERROR] {self.options.engine.title()} returned an error response. HTTP status code: {response.status_code}')
            return ''
        except requests.exceptions.RequestException as e:
            _warning(f'[WARNING] Request error: {e}')
            return ''

    def print_output(self, string: str) -> None:
        """Print a string to output file or terminal pager"""
        if self.options.view and self.pager:
            pager_cmd = self.pager
            if self.pager == 'less':
                pager_cmd += ' -R'

            try:
                proc = subprocess.Popen(pager_cmd.split(), stdin=subprocess.PIPE, text=True)
                proc.communicate(input=string)
            except Exception:
                print(string)
        else:
            output_file = self.options.output or sys.stdout
            if hasattr(output_file, 'write'):
                output_file.write(string + '\n')
            else:
                with open(output_file, 'a') as f:
                    f.write(string + '\n')

    def get_translation(self, text: str, sl: str, tl: str, hl: str
                        , is_verbose: bool = False
                        # TODO: implement these features or remove
                        #, to_speech: bool = False
                        #, return_playlist: Optional[List] = None
                        #, return_il: Optional[List] = None
                        ) -> Translation:
        """Get the translation of a string"""
        return self._translate(text, sl, tl, hl, is_verbose)

    def file_translation(self, uri: str) -> None:
        """Translate a file"""
        # TODO: Test
        file_match = re.match(r'^file://(.*)$', uri)
        if file_match:
            temp_input = self.options.input
            temp_verbose = self.options.verbose

            self.options.input = file_match.group(1)
            self.options.verbose = False

            self.translate_main()

            self.options.input = temp_input
            self.options.verbose = temp_verbose

    def web_translation(self, uri: str, sl: str, tl: str, hl: str) -> None:
        """Start a browser session and translate a web page"""
        # TODO: Test
        url = self._web_translate_url(uri, sl, tl, hl)
        if url:
            self.print_output(url)
            if self.options.browser and self.options.browser != 'NONE':
                try:
                    subprocess.run([self.options.browser, url],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                except Exception:
                    pass

    def translate(self, text: str, source_lang: str, inline: bool = False) -> None:
        """Translate the source text into all target languages"""
        # Check source language
        if not get_code(source_lang):
            _warning(f'[WARNING] Unknown source language code: {source_lang}')
        elif is_rtl(source_lang) and not _has_fribidi():
            _warning(f'[WARNING] {get_name(source_lang)} is a right-to-left language, but FriBidi is not found.')

        # Check host language
        host_lang = self.options.host_lang
        if not get_code(host_lang):
            _warning(f'[WARNING] Unknown language code: {host_lang}, fallback to English: en')
            host_lang = 'en'
        elif is_rtl(host_lang) and not _has_fribidi():
            _warning(f'[WARNING] {get_name(host_lang)} is a right-to-left language, but FriBidi is not found.')

        # Process all target languages
        target_langs = self.options.target_langs or []
        for i, target_lang in enumerate(target_langs, 1):
            # Non-interactive verbose mode: separator between targets
            if not self.options.interactive and self.options.verbose and i > 1:
                separator = '-' * (self.options.width or 80)
                self.print_output(prettify('target-separator', separator))

            if inline and text.startswith('file://'):
                self.file_translation(text)
            elif inline and (text.startswith('http://') or text.startswith('https://')):
                self.web_translation(text, source_lang, target_lang, host_lang)
            else:

                if not self.options.no_translate:
                    translation = self.get_translation(
                        text, source_lang, target_lang, host_lang,
                        self.options.verbose,
                        #self.options.play_mode or self.options.download_audio,
                        #playlist, il
                    )
                    self.print_output(translation.tty_output)
                else:
                    # TODO: test if this works and has a use case
                    translation = Translation('', source_lang if source_lang != 'auto' else 'en', [])

                translation.identified_lang = translation.identified_lang or 'en'

                self.play_audio_multiple(translation.audio_fragments)

                #if self.options.download_audio:
                #    if self.options.play_mode != 2 and not self.options.no_translate:
                #        if playlist:
                #            last_item = playlist[-1]
                #            self._download_audio(last_item.get('text', ''), last_item.get('target_lang', ''))
                #    else:
                #        self._download_audio(text, identified_lang)

    def translate_from_all_source_langs(self, text: str, inline: bool = False) -> None:
        """Translate the source text from all source languages"""
        for i, source_lang in enumerate(self.options.source_langs):
            # Non-interactive verbose mode: separator between sources
            if not self.options.interactive and self.options.verbose and i > 1:
                separator = '-' * (self.options.width or 80)
                self.print_output(prettify('target-separator', separator))

            self.translate(text, source_lang, inline)

    def translate_main(self) -> None:
        """Read from input and translate each line"""
        if self.options.interactive:
            self._prompt()

        input_source = self.options.input or sys.stdin

        if input_source == sys.stdin or os.path.isfile(str(input_source)):
            lines = []
            if hasattr(input_source, 'read'):
                lines = input_source.read().splitlines()
            else:
                with open(input_source, 'r', encoding='utf-8') as f:
                    lines = f.read().splitlines()

            for i, line in enumerate(lines):
                if len(line.strip()) > 0:
                    # Non-interactive verbose mode: separator between sources
                    if not self.options.interactive and self.options.verbose and i > 0:
                        separator = self.options.get('chr-source-separator', '=') * self.options.get('width', 80)
                        self.print_output(prettify('source-separator', separator))

                    if self.options.interactive:
                        self._repl(line)
                    else:
                        self.translate_from_all_source_langs(line)
                else:
                    # Non-interactive brief mode: preserve line breaks
                    if not self.options.interactive and not self.options.verbose:
                        self.print_output(line)
        else:
            _error(f'[ERROR] File not found: {input_source}')

    def play_audio_multiple(self, fragments: List[Tuple[str, str]]):
        if self.options.audio_mode > 0 and self.options.audio_player:
            if self.options.audio_mode == 1:
                for text, lang in fragments:
                    self.play_audio_single(text, lang)
            elif self.options.audio_mode == 2:
                self.play_audio_single(*fragments[-1])

    def play_audio_single(self, text: str, lang: str):
        """Produce audio for text"""
        url = self.tts_url(text, lang)
        play_remote_audio(self.options.audio_player, url)

    def if_debug(self, result_parts: List[str], text: str):
        if self.options.debug:
            result_parts.append(prettify('debug', text))

    def indent(self, tabs: int, text: str):
        tab_width = self.options.indent or 4
        return ' ' * (tabs * tab_width) + text

    @abc.abstractmethod
    def initialize(self):
        pass

    @abc.abstractmethod
    def tts_url(self, text: str, lang: str):
        """Generate text-to-speech URL - to be implemented by specific engines"""
        pass

    @abc.abstractmethod
    def web_translate_url(self, uri: str, sl: str, tl: str, hl: str) -> str:
        """Generate web translation URL - to be implemented by specific engines"""
        pass

    @abc.abstractmethod
    def _translate(self, text: str, source_lang: str, target_lang: str, host_lang: str
                   , is_verbose: bool
                   # TODO: implement these features or remove
                   #, to_speech: bool
                   #, return_playlist: Optional[List]
                   #, return_il: Optional[List]
                   ) -> Translation:
        """Core translation function - to be implemented by specific engines.

        :return: Tuple[str, str]: formatted translator output and the identified language of the input"""
        pass

    def _download_audio(self, text: str, lang: str) -> None:
        """Download audio for text"""
        pass  # Placeholder

    def _prompt(self) -> None:
        """Show interactive prompt"""
        pass  # Placeholder

    def _repl(self, line: str) -> None:
        """Handle REPL interaction"""
        pass  # Placeholder
