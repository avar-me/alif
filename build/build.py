#!/usr/bin/env python3
"""Build site pages:
- comparison_table.html from templates/comparison_table.html & data/alphabet.csv
- index.html from templates/index.html & data/alphabet_latin.json
"""

import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Comparison table paths
CSV_PATH = ROOT / "data" / "alphabet.csv"
COMPARISON_TEMPLATE_PATH = ROOT / "templates" / "comparison_table.html"
COMPARISON_OUTPUT_PATH = ROOT / "comparison_table.html"

# Latin alphabet homepage paths
LATIN_JSON_PATH = ROOT / "data" / "alphabet_latin.json"
INDEX_TEMPLATE_PATH = ROOT / "templates" / "index.html"
INDEX_OUTPUT_PATH = ROOT / "index.html"

AVAR_ALPHABET_ORDER = [
    "а", "б", "в", "г", "гъ", "гь", "гӀ", "д", "е", "ж", "з", "и", "й",
    "к", "кӀ", "къ", "кь", "л", "лъ", "лӀ", "м", "н", "о", "п", "р", "с",
    "т", "тӀ", "у", "ф", "х", "хъ", "хь", "хӀ", "ц", "цӀ", "ч", "чӀ",
    "ш", "щ", "ъ", "э", "ю", "я", "ё",
]

# Display columns: (header label, csv field)
COLUMNS = [
    ("Cyrillic", "cyrillic"),
    ("avar.me", "avarme"),
    ("Scientific", "scientific"),
    ("Typing", "typing"),
    ("1932", "historical"),
    ("Umarilov", "umarilov"),
    ("Turk", "turk"),
    ("Said", "said"),
    ("Google", "google"),
    ("Forker", "forker"),
    ("Claprot", "claprot"),
    ("Graham", "graham"),
    ("ЦӀадаса", "tsadasa"),
    ("Dict", "frequency"),
    ("Wiki", "freq_wiki"),
]

FREQ_FIELDS = {"frequency", "freq_wiki"}


def esc(value: str) -> str:
    return html.escape(value or "")


def build_comparison_table() -> None:
    rows = []
    with CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            cyrillic = (row.get("phoneme_cyrillic") or "").strip()
            if not cyrillic:
                continue
            rows.append(
                {
                    "cyrillic": cyrillic,
                    "avarme": row.get("variant_avarme", ""),
                    "scientific": row.get("variant_scientific", ""),
                    "typing": row.get("variant_typing", ""),
                    "historical": row.get("variant_historical_1932", ""),
                    "umarilov": row.get("variant_umarilov", ""),
                    "turk": row.get("variant_turk", ""),
                    "said": row.get("variant_said", ""),
                    "google": row.get("variant_google", ""),
                    "forker": row.get("variant_forker", ""),
                    "claprot": row.get("variant_claprot", ""),
                    "graham": row.get("variant_graham", ""),
                    "tsadasa": row.get("variant_tsadasa", ""),
                    "frequency": row.get("frequency", ""),
                    "freq_wiki": row.get("freq_wiki", ""),
                }
            )

    order_map = {letter: idx for idx, letter in enumerate(AVAR_ALPHABET_ORDER)}
    rows.sort(key=lambda r: order_map.get(r["cyrillic"], 999))

    table_html = "\n".join(
        "                        <tr>"
        + "".join(
            f'<td class="freq">{esc(r[field])}</td>'
            if field in FREQ_FIELDS
            else f"<td>{esc(r[field])}</td>"
            for _, field in COLUMNS
        )
        + "</tr>"
        for r in rows
    )

    template = COMPARISON_TEMPLATE_PATH.read_text(encoding="utf-8")
    output = template.replace("<!-- Will be populated by build script -->", table_html)
    COMPARISON_OUTPUT_PATH.write_text(output, encoding="utf-8")
    print(f"Built {COMPARISON_OUTPUT_PATH} with {len(rows)} letters")


def build_index_page() -> None:
    with LATIN_JSON_PATH.open(encoding="utf-8") as f:
        letters = json.load(f)

    # 1. Build sticky quick-navigation bar
    nav_links = []
    for item in letters:
        nav_links.append(f'<a href="#letter-{item["id"]}" title="{esc(item["letter"])}">{esc(item["upper"])}</a>')
    nav_html = "\n                ".join(nav_links)

    # 2. Build letter cards
    cards_html = []
    for item in letters:
        words_html = []
        for w in item.get("words", []):
            words_html.append(
                f'                    <li class="word-item">\n'
                f'                        <span class="word-latin">{esc(w["latin"])}</span>\n'
                f'                        <span class="word-cyrillic">{esc(w["cyrillic"])}</span>\n'
                f'                        <span class="word-ru">{esc(w["ru"])}</span>\n'
                f'                    </li>'
            )
        words_section = "\n".join(words_html) if words_html else "                    <li class=\"word-item\">—</li>"

        phrases_html = []
        for p in item.get("phrases", []):
            phrases_html.append(
                f'                    <li class="phrase-item">\n'
                f'                        <div class="phrase-latin">{esc(p["latin"])}</div>\n'
                f'                        <div class="phrase-cyrillic">{esc(p["cyrillic"])}</div>\n'
                f'                        <div class="phrase-ru">{esc(p["ru"])}</div>\n'
                f'                    </li>'
            )
        phrases_section = "\n".join(phrases_html) if phrases_html else "                    <li class=\"phrase-item\">—</li>"

        card = (
            f'                <article class="letter-card" id="letter-{item["id"]}">\n'
            f'                    <div class="letter-card-header">\n'
            f'                        <div class="letter-glyph">{esc(item["letter"])}</div>\n'
            f'                        <div class="letter-badges">\n'
            f'                            <span class="badge badge-cyrillic">Кириллица: {esc(item["cyrillic"])}</span>\n'
            f'                            <span class="badge badge-ipa">{esc(item["ipa"])}</span>\n'
            f'                        </div>\n'
            f'                    </div>\n'
            f'                    <p class="letter-desc">{esc(item["desc"])}</p>\n'
            f'                    <div class="card-section">\n'
            f'                        <h4 class="card-section-title">Слова</h4>\n'
            f'                        <ul class="words-list">\n'
            f'{words_section}\n'
            f'                        </ul>\n'
            f'                    </div>\n'
            f'                    <div class="card-section">\n'
            f'                        <h4 class="card-section-title">Примеры в предложениях</h4>\n'
            f'                        <ul class="phrases-list">\n'
            f'{phrases_section}\n'
            f'                        </ul>\n'
            f'                    </div>\n'
            f'                </article>'
        )
        cards_html.append(card)

    all_cards_html = "\n\n".join(cards_html)

    template = INDEX_TEMPLATE_PATH.read_text(encoding="utf-8")
    output = template.replace("<!-- Will be populated with alphabet links by build script -->", nav_html)
    output = output.replace("<!-- Will be populated with letter cards by build script -->", all_cards_html)

    INDEX_OUTPUT_PATH.write_text(output, encoding="utf-8")
    print(f"Built {INDEX_OUTPUT_PATH} with {len(letters)} letters")


def main() -> None:
    build_comparison_table()
    build_index_page()


if __name__ == "__main__":
    main()
