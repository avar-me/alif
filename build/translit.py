#!/usr/bin/env python3
"""Cyrillic -> avar.me Latin transliteration for Avar text."""

import re

PALOCHKA = {"Ӏ": "ӏ", "I": "ӏ"}  # normalize capital palochka to the lowercase glyph for matching

# Cyrillic grapheme -> avar.me Latin, derived from data/alphabet.csv (variant_avarme).
# "в" is handled separately by VW_RULE (see rule-vw.txt).
GRAPHEME_MAP = {
    "гъ": "ğ",
    "гь": "h",
    "гӏ": "ġ",
    "кӏ": "ķ",
    "къ": "q",
    "кь": "kļ",
    "лъ": "ļ",
    "лӏ": "ł",
    "тӏ": "ť",
    "хъ": "kh",
    "хь": "xh",
    "хӏ": "ħ",
    "цӏ": "ć",
    "чӏ": "č",
    "щ": "şç",
    "а": "a",
    "б": "b",
    "г": "g",
    "д": "d",
    "е": "e",
    "ж": "j",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "x",
    "ц": "c",
    "ч": "ç",
    "ш": "ş",
    "ъ": "'",
    "э": "e",
    "ю": "yu",
    "я": "ya",
    "ё": "ö",
}

FALLBACK_MAP = {"ы": "y", "ь": ""}

VOWELS = set("аеиоуэюяёaeiouy")

# Ordered longest-first for tokenizing.
_KEYS = sorted(GRAPHEME_MAP.keys(), key=len, reverse=True)


def _normalize(ch: str) -> str:
    return PALOCHKA.get(ch, ch)


def tokenize(word: str):
    """Split a single word (letters only) into (surface, grapheme_key) tokens."""
    i = 0
    n = len(word)
    tokens = []
    norm = "".join(_normalize(c) for c in word).lower()
    while i < n:
        matched = None
        for key in _KEYS:
            klen = len(key)
            if norm[i : i + klen] == key:
                matched = key
                break
        if matched is None:
            matched = norm[i]
            klen = 1
        tokens.append((word[i : i + klen], matched))
        i += klen
    return tokens


def _translit_word(word: str, tokens=None) -> str:
    if tokens is None:
        tokens = tokenize(word)
    out = []
    for idx, (surface, key) in enumerate(tokens):
        if key == "в":
            next_is_vowel = False
            if idx + 1 < len(tokens):
                nxt_norm = tokens[idx + 1][1]
                first_char = nxt_norm[0] if nxt_norm else ""
                next_is_vowel = first_char in VOWELS
            if idx == 0 or not next_is_vowel:
                latin = "v"
            else:
                latin = "w"
        elif key in GRAPHEME_MAP:
            latin = GRAPHEME_MAP[key]
        else:
            latin = FALLBACK_MAP.get(key, key)
        if word.isupper() and len(word) > 1:
            latin = latin.upper()
        elif surface[0].isupper() and latin:
            latin = latin[0].upper() + latin[1:]
        out.append(latin)
    return "".join(out)


_WORD_RE = re.compile(r"[а-яёӀӏ]+", re.IGNORECASE)


def translit_text(text: str) -> str:
    """Transliterate a whole phrase, preserving spaces/punctuation."""

    def repl(m):
        return _translit_word(m.group(0))

    return _WORD_RE.sub(repl, text)


def graphemes_in(word: str):
    return {key for _, key in tokenize(word) if key != "в" or True}
