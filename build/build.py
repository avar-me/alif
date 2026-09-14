#!/usr/bin/env python3
"""Fill the alphabet table in templates/index.html from data/alphabet.csv."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "alphabet.csv"
TEMPLATE_PATH = ROOT / "templates" / "index.html"
OUTPUT_PATH = ROOT / "index.html"

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


def cell(value: str) -> str:
    return (value or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> None:
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
            f'<td class="freq">{cell(r[field])}</td>'
            if field in FREQ_FIELDS
            else f"<td>{cell(r[field])}</td>"
            for _, field in COLUMNS
        )
        + "</tr>"
        for r in rows
    )

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    output = template.replace("<!-- Will be populated by build script -->", table_html)
    OUTPUT_PATH.write_text(output, encoding="utf-8")
    print(f"Built {OUTPUT_PATH} with {len(rows)} letters")


if __name__ == "__main__":
    main()
