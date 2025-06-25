import abc
import argparse
import base64
import os
import re
import socket
import subprocess
import sys
from typing import List, Optional
from urllib.parse import quote, unquote

import requests
from requests.auth import HTTPBasicAuth

from src.langdata import get_code
from src.misc import prettify


def _has_fribidi() -> bool:
    """Check if FriBidi is available"""
    try:
        subprocess.run(['fribidi', '--version'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def is_rtl(lang: str) -> bool:
    """Check if language is right-to-left"""
    rtl_languages = ['ar', 'he', 'fa', 'ur', 'yi', 'iw']
    return lang in rtl_languages


def _starts_with_any(text: str, prefixes: List[str]) -> Optional[str]:
    """Check if text starts with any of the given prefixes"""
    for prefix in prefixes:
        if text.startswith(prefix):
            return prefix
    return None


def _error(message: str) -> None:
    """Print error message"""
    print(message, file=sys.stderr)


def _warning(message: str) -> None:
    """Print warning message"""
    print(message, file=sys.stderr)


URI_SCHEMES = ['http://', 'https://', 'file://', 'ftp://']


def preprocess(text: str) -> str:
    """Pre-process string (URL-encode before send)"""
    return quote(text)


def preprocess_by_dump(text: str) -> str:
    """Pre-process string using hexdump to URL-encode everything"""
    encoded = ""
    for char in text.encode('utf-8'):
        encoded += f'%{char:02x}'
    return encoded


def postprocess(text: str) -> str:
    """Post-process string (remove any redundant whitespace)"""
    # Remove space before punctuation
    text = re.sub(r" ([.,;:?!'])", r'\1', text)
    # Remove space after opening quotes
    text = re.sub(r"(') ", r'\1', text)
    return text


class TranslationEngine(metaclass=abc.ABCMeta):
    """Main translation engine class"""

    def __init__(self, options: argparse.Namespace):
        self.options: argparse.Namespace = options
        self.http_service = None
        self.http_host = ""
        self.http_port = 80
        self.http_path_prefix = ""
        self.http_proxy_spec = {}
        self.http_auth_user = ""
        self.http_auth_pass = ""
        self.http_auth_credentials = ""
        self.cookie = ""
        self.pager = ""
        self.dump_content_lengths = {}

    def init_http_service(self) -> None:
        """Initialize HTTP service connection"""
        inet = 'inet'
        if self.options.ip_version:
            inet = f'inet{self.options['ip-version']}'

        if self.options.proxy:
            proxy_match = re.match(
                r'^(http://)??(([^:]+):([^@]+)@)?([^/]*):([^/:]*)$',
                self.options['proxy']
            )
            if proxy_match:
                self.http_auth_user = proxy_match.group(3) or ""
                self.http_auth_pass = proxy_match.group(4) or ""
                if self.http_auth_user and self.http_auth_pass:
                    credentials = f'{unquote(self.http_auth_user)}:{self.http_auth_pass}'
                    self.http_auth_credentials = base64.b64encode(
                        credentials.encode()).decode()
                self.http_service = f'/{inet}/tcp/0/{proxy_match.group(5)}/{proxy_match.group(6)}'
                self.http_path_prefix = f'http://{self.http_host}'
        else:
            self.http_service = f'/{inet}/tcp/0/{self.http_host}/{self.http_port}'
            self.http_path_prefix = ""

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
            # Make the request with automatic redirect handling
            response = requests.get(
                url,
                headers=headers,
                cookies=cookies,
                auth=auth,
                timeout=30,  # Add timeout for better error handling
                allow_redirects=True  # Handle redirects automatically
            )

            # Handle different status codes
            if response.status_code == 429:
                _error(
                    f'[ERROR] {self.options.engine.title()} did not return results because rate limiting is in effect')
                return ""

            # Raise an exception for HTTP error status codes (4xx, 5xx)
            response.raise_for_status()

            return response.text

        except requests.exceptions.Timeout:
            _warning('[WARNING] Request timed out')
            return ""
        except requests.exceptions.ConnectionError as e:
            _warning(f'[WARNING] Connection error: {e}')
            return ""
        except requests.exceptions.HTTPError as e:
            _error(
                f'[ERROR] {self.options.engine.title()} returned an error response. HTTP status code: {response.status_code}')
            return ""
        except requests.exceptions.RequestException as e:
            _warning(f'[WARNING] Request error: {e}')
            return ""

    def http_get_old(self, url: str) -> str:
        """Send an HTTP GET request and get response from online translator"""
        headers = {
            'Host': self.http_host,
            'Connection': 'close'
        }

        if self.options.user_agent:
            headers['User-Agent'] = self.options.user_agent
        if self.cookie:
            headers['Cookie'] = self.cookie
        if self.http_auth_user and self.http_auth_pass:
            headers['Proxy-Authorization'] = f'Basic {self.http_auth_credentials}'

        # Create HTTP request
        header_str = f'GET {url} HTTP/1.1\r\n'
        for key, value in headers.items():
            header_str += f'{key}: {value}\r\n'
        header_str += '\r\n'

        content = ""
        status = ""
        location = ""

        try:
            # This is a simplified version - in practice you'd need proper socket handling
            # or use requests library for HTTP communication
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.http_host, self.http_port))
            sock.send(header_str.encode())

            response = b""
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                response += data

            sock.close()

            # Parse response
            response_str = response.decode('utf-8', errors='ignore')
            header_end = response_str.find('\r\n\r\n')
            if header_end != -1:
                header_part = response_str[:header_end]
                content = response_str[header_end + 4:]

                # Extract status and location from headers
                status_match = re.search(r'HTTP[^ ]* ([^ ]*)', header_part)
                if status_match:
                    status = status_match.group(1)

                location_match = re.search(r'Location: (.*)', header_part)
                if location_match:
                    location = location_match.group(1).strip()

        except Exception as e:
            _warning(f'[WARNING] Connection error: {e}')
            return ""

        # Handle redirects and errors
        if status in ['301', '302'] and location:
            # Handle redirect - would need to implement curl equivalent
            pass
        elif status == '429':
            _error(
                f'[ERROR] {self.options.engine.title()} did not return results because rate limiting is in effect')
            return ""
        elif status and int(status) >= 400:
            _error(
                f'[ERROR] {self.options.engine.title()} returned an error response. HTTP status code: {status}')
            return ""

        return content or ""

    def post_response(self, text: str, sl: str, tl: str, hl: str, req_type: str = "") -> str:
        """Send an HTTP POST request and return response from online translator"""
        url = self._post_request_url(text, sl, tl, hl, req_type)
        content_type = _post_request_content_type(text, sl, tl, hl, req_type)
        user_agent = self._post_request_user_agent(text, sl, tl, hl, req_type)
        req_body = self._post_request_body(text, sl, tl, hl, req_type)

        content_length = len(req_body.encode('utf-8'))

        headers = {
            'Host': self.http_host,
            'Connection': 'close',
            'Content-Length': str(content_length),
            'Content-Type': content_type
        }

        if self.options.user_agent and not user_agent:
            headers['User-Agent'] = self.options.user_agent
        if user_agent:
            headers['User-Agent'] = user_agent
        if self.cookie:
            headers['Cookie'] = self.cookie
        if self.http_auth_user and self.http_auth_pass:
            headers['Proxy-Authorization'] = f'Basic {self.http_auth_credentials}'

        # Create HTTP request
        header_str = f'POST {url} HTTP/1.1\r\n'
        for key, value in headers.items():
            header_str += f'{key}: {value}\r\n'
        header_str += f'\r\n{req_body}'

        # Similar socket handling as in get_response
        # Implementation would be similar to get_response but with POST
        return ""  # Placeholder

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
                        ) -> str:
        """Get the translation of a string"""
        return self._translate(text, sl, tl, hl, is_verbose)

    def file_translation(self, uri: str) -> None:
        """Translate a file"""
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
            lang_name = self._get_name(source_lang)
            _warning(f'[WARNING] {lang_name} is a right-to-left language, but FriBidi is not found.')

        # Check host language
        host_lang = self.options.host_lang
        if not get_code(host_lang):
            _warning(f'[WARNING] Unknown language code: {host_lang}, fallback to English: en')
            host_lang = 'en'
        elif is_rtl(host_lang) and not _has_fribidi():
            lang_name = self._get_name(host_lang)
            _warning(f'[WARNING] {lang_name} is a right-to-left language, but FriBidi is not found.')

        # Process all target languages
        target_langs = self.options.target_langs or []
        for i, target_lang in enumerate(target_langs, 1):
            # Non-interactive verbose mode: separator between targets
            if not self.options.interactive and self.options.verbose and i > 1:
                separator = '-' * (self.options.width or 80)
                self.print_output(prettify('target-separator', separator))

            if inline and _starts_with_any(text, URI_SCHEMES) == 'file://':
                self.file_translation(text)
            elif inline and _starts_with_any(text, URI_SCHEMES) in ['http://', 'https://']:
                self.web_translation(text, source_lang, target_lang, host_lang)
            else:
                playlist = []
                il = [] # TODO: rename

                if not self.options.no_translate:
                    translation = self.get_translation(
                        text, source_lang, target_lang, host_lang,
                        self.options.verbose,
                        #self.options.play_mode or self.options.download_audio,
                        #playlist, il
                    )
                    self.print_output(translation)
                else:
                    il.append(source_lang if source_lang != 'auto' else 'en')

                self._produce_audio(playlist, text, il[0] if il else 'en')

                if self.options.download_audio:
                    if self.options.play_mode != 2 and not self.options.no_translate:
                        if playlist:
                            last_item = playlist[-1]
                            self._download_audio(last_item.get('text', ''), last_item.get('target_lang', ''))
                    else:
                        self._download_audio(text, il[0] if il else 'en')

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

    @abc.abstractmethod
    def initialize(self):
        pass

    @abc.abstractmethod
    def post_request_url(self, text: str, sl: str, tl: str, hl: str, req_type: str) -> str:
        """Generate POST request URL - to be implemented by specific engines"""
        pass

    @abc.abstractmethod
    def post_request_content_type(self, text: str, sl: str, tl: str, hl: str, req_type: str) -> str:
        """Get POST request content type - to be implemented by specific engines"""
        #return 'application/x-www-form-urlencoded'
        pass

    @abc.abstractmethod
    def post_request_user_agent(self, text: str, sl: str, tl: str, hl: str, req_type: str) -> str:
        """Get POST request user agent - to be implemented by specific engines"""
        pass

    @abc.abstractmethod
    def post_request_body(self, text: str, sl: str, tl: str, hl: str, req_type: str) -> str:
        """Generate POST request body - to be implemented by specific engines"""
        pass

    @abc.abstractmethod
    def tts_url(self, text: str, tl: str):
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
                   ) -> str:
        """Core translation function - to be implemented by specific engines"""
        pass






    def _get_name(self, lang: str) -> str:
        """Get language name from code"""
        return lang  # Placeholder

    def _produce_audio(self, playlist: List, text: str, lang: str) -> None:
        """Produce audio for text"""
        pass  # Placeholder

    def _download_audio(self, text: str, lang: str) -> None:
        """Download audio for text"""
        pass  # Placeholder

    def _prompt(self) -> None:
        """Show interactive prompt"""
        pass  # Placeholder

    def _repl(self, line: str) -> None:
        """Handle REPL interaction"""
        pass  # Placeholder
