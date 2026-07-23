from __future__ import annotations

_NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
}


def _coerce_count(count: int | None, user_text: str | None) -> int:
    if isinstance(count, int) and count > 0:
        return count

    if user_text:
        for token in user_text.lower().replace("-", " ").split():
            if token.isdigit():
                parsed = int(token)
                if parsed > 0:
                    return parsed
            if token in _NUMBER_WORDS and _NUMBER_WORDS[token] > 0:
                return _NUMBER_WORDS[token]

    return 1


def print_i_like_tacos(count: int | None = None, user_text: str | None = None) -> str:
    total = _coerce_count(count, user_text)
    lines = ["I LIKE TACOS" for _ in range(total)]
    output = "\n".join(lines)
    print(output)
    return output


print_i_like_tacos_schema = {
    "type": "function",
    "function": {
        "name": "print_i_like_tacos",
        "description": "Print 'I LIKE TACOS' the requested number of times.",
        "parameters": {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "description": "How many times to print the phrase.",
                    "minimum": 1,
                },
                "user_text": {
                    "type": "string",
                    "description": "The user's original text, used to infer a count when one is not explicit.",
                },
            },
            "required": [],
        },
    },
}

print_i_like_tacos_spec = {
    "name": "print_i_like_tacos",
    "function": print_i_like_tacos,
    "schema": print_i_like_tacos_schema,
    "terminal": True,
}
