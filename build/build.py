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


def cell(value: str) -> str:
    return (value or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> None:
    rows = []
    with CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        for row in reader:
            if len(row) < 7 or not row[1]:
                continue
            rows.append(
                {
                    "cyrillic": row[1],
                    "avarme": row[2],
                    "scientific": row[4],
                    "typing": row[6],
                    "historical": row[7] if len(row) > 7 else "",
                    "umarilov": row[9] if len(row) > 9 else "",
                    "turk": row[10] if len(row) > 10 else "",
                    "said": row[11] if len(row) > 11 else "",
                    "google": row[12] if len(row) > 12 else "",
                    "frequency": row[13] if len(row) > 13 else "",
                    "freq_wiki": row[14] if len(row) > 14 else "",
                }
            )

    order_map = {letter: idx for idx, letter in enumerate(AVAR_ALPHABET_ORDER)}
    rows.sort(key=lambda r: order_map.get(r["cyrillic"], 999))

    table_html = "\n".join(
        (
            "                        <tr>"
            f"<td>{cell(r['cyrillic'])}</td>"
            f"<td>{cell(r['avarme'])}</td>"
            f"<td>{cell(r['scientific'])}</td>"
            f"<td>{cell(r['typing'])}</td>"
            f"<td>{cell(r['historical'])}</td>"
            f"<td>{cell(r['umarilov'])}</td>"
            f"<td>{cell(r['turk'])}</td>"
            f"<td>{cell(r['said'])}</td>"
            f"<td>{cell(r['google'])}</td>"
            f"<td class=\"freq\">{cell(r['frequency'])}</td>"
            f"<td class=\"freq\">{cell(r['freq_wiki'])}</td>"
            "</tr>"
        )
        for r in rows
    )

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    output = template.replace("<!-- Will be populated by build script -->", table_html)
    OUTPUT_PATH.write_text(output, encoding="utf-8")
    print(f"Built {OUTPUT_PATH} with {len(rows)} letters")


if __name__ == "__main__":
    main()
