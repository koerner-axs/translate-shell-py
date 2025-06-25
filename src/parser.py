import re
from typing import Dict, List, Any, Optional


NULLSTR = ''
SUBSEP = '\x1C'  # ASCII File Separator, mimicking AWK's SUBSEP


def belongs_to(char: str, char_list: List[str]) -> bool:
    """Check if a character belongs to a list of characters."""
    return char in char_list


def starts_with_any(string: str, patterns: List[str]) -> Optional[str]:
    """Check if string starts with any of the patterns, return the matching pattern."""
    for pattern in patterns:
        if string.startswith(pattern):
            return pattern
    return None


def matches_any(string: str, patterns: List[str]) -> Optional[str]:
    """Check if string matches any of the regex patterns, return the matching pattern."""
    for pattern in patterns:
        if re.match(f"^{pattern}", string):
            return pattern
    return None


def unparameterize(token: str) -> str:
    """Remove quotes from a token if it's quoted."""
    if len(token) >= 2 and token[0] == token[-1] and token[0] in ['"', "'"]:
        return token[1:-1]
    return token


def is_numeric(value: Any) -> bool:
    """Check if a value is numeric (mimicking AWK's isnum)."""
    try:
        float(str(value))
        return True
    except (ValueError, TypeError):
        return False





def tokenize(string: str) -> List[str]:
    """
    Tokenize a string and return a token list.

    Args:
        string: The input string to tokenize

    Returns:
        List of tokens
    """
    delimiters: Optional[List[str]] = [" ", "\t", "\v"]  # whitespace, horizontal tab, vertical tab
    newlines: Optional[List[str]] = ["\n", "\r"]  # line feed, carriage return
    quotes: Optional[List[str]] = ['"']  # double quote
    escape_chars: Optional[List[str]] = ["\\"]  # backslash
    left_block_comments: Optional[List[str]] = ["#|", "/*", "(*"]  # Lisp, C, ML style
    right_block_comments: Optional[List[str]] = ["|#", "*/", "*)"]  # Lisp, C, ML style
    line_comments: Optional[List[str]] = [";", "//", "#"]  # Lisp, C++, hash style
    reserved_operators: Optional[List[str]] = ["(", ")", "[", "]", "{", "}", ","]
    reserved_patterns: Optional[List[str]] = [
        r"[+-]?((0|[1-9][0-9]*)|[.][0-9]*|(0|[1-9][0-9]*)[.][0-9]*)([Ee][+-]?[0-9]+)?",  # scientific notation
        r"[+-]?0[0-7]+([.][0-7]*)?",  # octal
        r"[+-]?0[Xx][0-9A-Fa-f]+([.][0-9A-Fa-f]*)?",  # hexadecimal
    ]

    tokens = []
    s = list(string)  # Split string into characters
    current_token = ""
    quoting = escaping = block_commenting = line_commenting = False
    i = 0

    while i < len(s):
        c = s[i]
        r = string[i:]  # Remaining string from position i

        if block_commenting:
            temp_string = starts_with_any(r, right_block_comments)
            if temp_string:
                block_commenting = False  # block comment ends
                i += len(temp_string)
            else:
                i += 1

        elif line_commenting:
            if belongs_to(c, newlines):
                line_commenting = False  # line comment ends
            i += 1

        elif quoting:
            current_token += c

            if escaping:
                escaping = False  # escape ends
            else:
                if belongs_to(c, quotes):
                    # Finish the current token
                    if current_token:
                        tokens.append(current_token)
                        current_token = ""
                    quoting = False  # quotation ends
                elif belongs_to(c, escape_chars):
                    escaping = True  # escape begins

            i += 1

        else:
            if belongs_to(c, delimiters) or belongs_to(c, newlines):
                # Finish the current token
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                i += 1

            elif belongs_to(c, quotes):
                # Finish the current token
                if current_token:
                    tokens.append(current_token)
                current_token = c
                quoting = True  # quotation begins
                i += 1

            elif temp_string := starts_with_any(r, left_block_comments):
                # Finish the current token
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                block_commenting = True  # block comment begins
                i += len(temp_string)

            elif temp_string := starts_with_any(r, line_comments):
                # Finish the current token
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                line_commenting = True  # line comment begins
                i += len(temp_string)

            elif temp_string := starts_with_any(r, reserved_operators):
                # Finish the current token
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                # Reserve token
                tokens.append(temp_string)
                i += len(temp_string)

            elif temp_pattern := matches_any(r, reserved_patterns):
                # Finish the current token
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                # Reserve token
                match = re.match(f"^{temp_pattern}", r)
                if match:
                    matched_text = match.group(0)
                    tokens.append(matched_text)
                    i += len(matched_text)
                else:
                    i += 1

            else:
                # Continue with the current token
                current_token += c
                i += 1

    # Finish the last token
    if current_token:
        tokens.append(current_token)

    return tokens


def parse_json_array(tokens: List[str]) -> Dict[str, str]:
    """
    Parse a token list of JSON array and return an AST.

    Args:
        tokens: List of tokens to parse

    Returns:
        Dictionary representing the AST
    """
    json_left_brackets = ['(', '[', '{']
    json_right_brackets = [')', ']', '}']
    json_separators = [',']

    ast = {}
    stack = [0]
    p = 0

    for token in tokens:
        if belongs_to(token, json_left_brackets):
            p += 1
            stack.append(0)
        elif belongs_to(token, json_right_brackets):
            stack.pop()
            p -= 1
        elif belongs_to(token, json_separators):
            stack[p] += 1
        else:
            key = str(stack[0])
            for j in range(1, p + 1):
                key += SUBSEP + str(stack[j])
            ast[key] = token

    return ast


def parse_json(tokens: List[str]) -> Dict[str, str]:
    """
    JSON parser.

    Args:
        tokens: List of tokens to parse

    Returns:
        Dictionary representing the parsed JSON AST
    """
    array_start_tokens = ["["]
    array_end_tokens = ["]"]
    object_start_tokens = ["{"]
    object_end_tokens = ["}"]
    commas = [","]
    colons = [":"]

    ast = {}
    stack = [0]
    p = 0
    flag = False  # ready to read key

    for token in tokens:
        if belongs_to(token, array_start_tokens):
            p += 1
            stack.append(0)
        elif belongs_to(token, object_start_tokens):
            p += 1
            stack.append(NULLSTR)
            flag = False  # ready to read key
        elif (belongs_to(token, object_end_tokens) or
              belongs_to(token, array_end_tokens)):
            stack.pop()
            p -= 1
        elif belongs_to(token, commas):
            if is_numeric(stack[p]):  # array
                stack[p] += 1  # increase index
            else:  # object
                flag = False  # ready to read key
        elif belongs_to(token, colons):
            flag = True  # ready to read value
        elif is_numeric(stack[p]) or flag:
            # Read a value
            key = str(stack[0])
            for j in range(1, p + 1):
                key += SUBSEP + str(stack[j])
            ast[key] = token
            flag = False  # ready to read key
        else:
            # Read a key
            stack[p] = unparameterize(token)

    return ast


def parse_list(tokens: List[str]) -> Dict[str, Dict[int, str]]:
    """
    S-expr parser.

    Args:
        tokens: List of tokens to parse

    Returns:
        Dictionary representing the parsed S-expression AST
    """
    left_brackets = ["(", "[", "{"]
    right_brackets = [")", "]", "}"]
    separators = [","]

    ast = {}
    stack = [0]
    p = 0

    for token in tokens:
        if belongs_to(token, left_brackets):
            p += 1
            stack.append(0)
        elif belongs_to(token, right_brackets):
            stack[p - 1] += 1
            stack.pop()
            p -= 1
        elif belongs_to(token, separators):
            pass
        else:
            key = NULLSTR
            if p > 0:
                for j in range(p - 1):
                    if key == NULLSTR:
                        key = str(stack[j])
                    else:
                        key += SUBSEP + str(stack[j])

                # Initialize nested dict if needed
                if key not in ast:
                    ast[key] = {}
                ast[key][stack[p - 1]] = NULLSTR

                if key == NULLSTR:
                    key = str(stack[p - 1])
                else:
                    key += SUBSEP + str(stack[p - 1])

            # Initialize nested dict if needed
            if key not in ast:
                ast[key] = {}
            ast[key][stack[p]] = token
            stack[p] += 1

    return ast


if __name__ == "__main__":
    # Test tokenization
    test_string = 'hello "world" (test) [1,2,3] /* comment */ // line comment'
    out = tokenize(test_string)
    print("Tokens:", out)

    # Test JSON array parsing
    json_tokens = ["[", "1", ",", "2", ",", "3", "]"]
    json_ast = parse_json_array(json_tokens)
    print("JSON Array AST:", json_ast)

    # Test JSON parsing
    json_tokens2 = ["{", '"key"', ":", '"value"', ",", '"num"', ":", "42", "}"]
    json_ast2 = parse_json(json_tokens2)
    print("JSON AST:", json_ast2)

    # Test S-expr parsing
    sexpr_tokens = ["(", "add", "1", "2", ")"]
    sexpr_ast = parse_list(sexpr_tokens)
    print("S-expr AST:", sexpr_ast)
