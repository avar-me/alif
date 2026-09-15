#!/usr/bin/env python3
"""Extract curated words and example sentences for each Avar Latin letter from av-ru.jsonl."""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from translit import tokenize, translit_text, _translit_word  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT.parent / "sources" / "data" / "av-ru.jsonl"
OUTPUT = ROOT / "data" / "alphabet_latin.json"

WORD_RE = re.compile(r"[а-яёӀӏ]+", re.IGNORECASE)


def norm(s: str) -> str:
    return s.replace("Ӏ", "ӏ").replace("I", "ӏ")


LATIN_LETTERS = [
    {
        "id": "a",
        "letter": "A a",
        "upper": "A",
        "lower": "a",
        "cyrillic": "А а",
        "ipa": "[a]",
        "desc": "Неогубленный гласный переднего/среднего ряда нижнего подъёма.",
        "cyr_keys": ["а"],
    },
    {
        "id": "b",
        "letter": "B b",
        "upper": "B",
        "lower": "b",
        "cyrillic": "Б б",
        "ipa": "[b]",
        "desc": "Звонкий губно-губной смычный согласный.",
        "cyr_keys": ["б"],
    },
    {
        "id": "c",
        "letter": "C c",
        "upper": "C",
        "lower": "c",
        "cyrillic": "Ц ц",
        "ipa": "[t͡s]",
        "desc": "Глухая переднеязычная свистящая аффриката.",
        "cyr_keys": ["ц"],
    },
    {
        "id": "c-acute",
        "letter": "Ć ć",
        "upper": "Ć",
        "lower": "ć",
        "cyrillic": "ЦӀ цӀ",
        "ipa": "[t͡sʼ]",
        "desc": "Эйективная (абруптивная) переднеязычная свистящая аффриката.",
        "cyr_keys": ["цӀ"],
    },
    {
        "id": "c-cedilla",
        "letter": "Ç ç",
        "upper": "Ç",
        "lower": "ç",
        "cyrillic": "Ч ч",
        "ipa": "[t͡ʃ]",
        "desc": "Глухая переднеязычная шипящая аффриката.",
        "cyr_keys": ["ч"],
    },
    {
        "id": "c-caron",
        "letter": "Č č",
        "upper": "Č",
        "lower": "č",
        "cyrillic": "ЧӀ чӀ",
        "ipa": "[t͡ʃʼ]",
        "desc": "Эйективная (абруптивная) переднеязычная шипящая аффриката.",
        "cyr_keys": ["чӀ"],
    },
    {
        "id": "d",
        "letter": "D d",
        "upper": "D",
        "lower": "d",
        "cyrillic": "Д д",
        "ipa": "[d]",
        "desc": "Звонкий переднеязычный смычный согласный.",
        "cyr_keys": ["д"],
    },
    {
        "id": "e",
        "letter": "E e",
        "upper": "E",
        "lower": "e",
        "cyrillic": "Е е, Э э",
        "ipa": "[e]",
        "desc": "Неогубленный гласный переднего ряда среднего подъёма.",
        "cyr_keys": ["е", "э"],
    },
    {
        "id": "f",
        "letter": "F f",
        "upper": "F",
        "lower": "f",
        "cyrillic": "Ф ф",
        "ipa": "[f]",
        "desc": "Глухой губно-зубной щелевой согласный (в заимствованных словах).",
        "cyr_keys": ["ф"],
    },
    {
        "id": "g",
        "letter": "G g",
        "upper": "G",
        "lower": "g",
        "cyrillic": "Г г",
        "ipa": "[ɡ]",
        "desc": "Звонкий заднеязычный смычный согласный.",
        "cyr_keys": ["г"],
    },
    {
        "id": "g-breve",
        "letter": "Ğ ğ",
        "upper": "Ğ",
        "lower": "ğ",
        "cyrillic": "Гъ гъ",
        "ipa": "[ʁ]",
        "desc": "Звонкий увулярный спирант (фрикатив).",
        "cyr_keys": ["гъ"],
    },
    {
        "id": "g-dot",
        "letter": "Ġ ġ",
        "upper": "Ġ",
        "lower": "ġ",
        "cyrillic": "ГӀ гӀ",
        "ipa": "[ʕ]",
        "desc": "Звонкий фарингальный согласный (гортанный эпиглоттальный).",
        "cyr_keys": ["гӀ"],
    },
    {
        "id": "h",
        "letter": "H h",
        "upper": "H",
        "lower": "h",
        "cyrillic": "Гь гь",
        "ipa": "[h]",
        "desc": "Глухой глоттальный (гортанный) щелевой согласный.",
        "cyr_keys": ["гь"],
    },
    {
        "id": "h-stroke",
        "letter": "Ħ ħ",
        "upper": "Ħ",
        "lower": "ħ",
        "cyrillic": "ХӀ хӀ",
        "ipa": "[ħ]",
        "desc": "Глухой фарингальный щелевой согласный.",
        "cyr_keys": ["хӀ"],
    },
    {
        "id": "i",
        "letter": "I i",
        "upper": "I",
        "lower": "i",
        "cyrillic": "И и",
        "ipa": "[i]",
        "desc": "Неогубленный гласный переднего ряда верхнего подъёма.",
        "cyr_keys": ["и"],
    },
    {
        "id": "j",
        "letter": "J j",
        "upper": "J",
        "lower": "j",
        "cyrillic": "Ж ж",
        "ipa": "[ʒ]",
        "desc": "Звонкий переднеязычный шипящий согласный.",
        "cyr_keys": ["ж"],
    },
    {
        "id": "k",
        "letter": "K k",
        "upper": "K",
        "lower": "k",
        "cyrillic": "К к",
        "ipa": "[k]",
        "desc": "Глухой заднеязычный смычный согласный.",
        "cyr_keys": ["к"],
    },
    {
        "id": "k-cedilla",
        "letter": "Ķ ķ",
        "upper": "Ķ",
        "lower": "ķ",
        "cyrillic": "КӀ кӀ",
        "ipa": "[kʼ]",
        "desc": "Эйективный (абруптивный) заднеязычный смычный согласный.",
        "cyr_keys": ["кӀ"],
    },
    {
        "id": "q",
        "letter": "Q q",
        "upper": "Q",
        "lower": "q",
        "cyrillic": "Къ къ",
        "ipa": "[qʼ]",
        "desc": "Эйективный увулярный смычный согласный / аффриката.",
        "cyr_keys": ["къ"],
    },
    {
        "id": "kl-stroke",
        "letter": "Kļ kļ",
        "upper": "Kļ",
        "lower": "kļ",
        "cyrillic": "Кь кь",
        "ipa": "[t͡ɬʼ]",
        "desc": "Эйективная боковая (латеральная) аффриката.",
        "cyr_keys": ["кь"],
    },
    {
        "id": "l",
        "letter": "L l",
        "upper": "L",
        "lower": "l",
        "cyrillic": "Л л",
        "ipa": "[l]",
        "desc": "Звонкий переднеязычный боковой сонант.",
        "cyr_keys": ["л"],
    },
    {
        "id": "l-cedilla",
        "letter": "Ļ ļ",
        "upper": "Ļ",
        "lower": "ļ",
        "cyrillic": "Лъ лъ",
        "ipa": "[ɬ]",
        "desc": "Глухой боковой (латеральный) щелевой согласный.",
        "cyr_keys": ["лъ"],
    },
    {
        "id": "l-stroke",
        "letter": "Ł ł",
        "upper": "Ł",
        "lower": "ł",
        "cyrillic": "ЛӀ лӀ",
        "ipa": "[t͡ɬ]",
        "desc": "Глухая боковая аффриката. Исторический и диалектный звук аварского языка; в совр. стандарте сблизился с «лъ».",
        "cyr_keys": ["лӀ"],
    },
    {
        "id": "m",
        "letter": "M m",
        "upper": "M",
        "lower": "m",
        "cyrillic": "М м",
        "ipa": "[m]",
        "desc": "Носовой губно-губной сонант.",
        "cyr_keys": ["м"],
    },
    {
        "id": "n",
        "letter": "N n",
        "upper": "N",
        "lower": "n",
        "cyrillic": "Н н",
        "ipa": "[n]",
        "desc": "Носовой переднеязычный сонант.",
        "cyr_keys": ["н"],
    },
    {
        "id": "o",
        "letter": "O o",
        "upper": "O",
        "lower": "o",
        "cyrillic": "О о",
        "ipa": "[o]",
        "desc": "Огубленный гласный заднего ряда среднего подъёма.",
        "cyr_keys": ["о"],
    },
    {
        "id": "o-umlaut",
        "letter": "Ö ö",
        "upper": "Ö",
        "lower": "ö",
        "cyrillic": "Ё ё",
        "ipa": "[ø]",
        "desc": "Огубленный гласный переднего ряда (в диалектах и заимствованиях).",
        "cyr_keys": ["ё"],
    },
    {
        "id": "p",
        "letter": "P p",
        "upper": "P",
        "lower": "p",
        "cyrillic": "П п",
        "ipa": "[p]",
        "desc": "Глухой губно-губной смычный согласный.",
        "cyr_keys": ["п"],
    },
    {
        "id": "r",
        "letter": "R r",
        "upper": "R",
        "lower": "r",
        "cyrillic": "Р р",
        "ipa": "[r]",
        "desc": "Переднеязычный дрожащий согласный (вибрант).",
        "cyr_keys": ["р"],
    },
    {
        "id": "s",
        "letter": "S s",
        "upper": "S",
        "lower": "s",
        "cyrillic": "С с",
        "ipa": "[s]",
        "desc": "Глухой переднеязычный свистящий согласный.",
        "cyr_keys": ["с"],
    },
    {
        "id": "s-cedilla",
        "letter": "Ş ş",
        "upper": "Ş",
        "lower": "ş",
        "cyrillic": "Ш ш",
        "ipa": "[ʃ]",
        "desc": "Глухой переднеязычный шипящий согласный.",
        "cyr_keys": ["ш"],
    },
    {
        "id": "sc-cedilla",
        "letter": "Şç şç",
        "upper": "Şç",
        "lower": "şç",
        "cyrillic": "Щ щ",
        "ipa": "[ʃː] / [ʃt͡ʃ]",
        "desc": "Долгий шипящий или сложная аффриката (в заимствованиях).",
        "cyr_keys": ["щ"],
    },
    {
        "id": "t",
        "letter": "T t",
        "upper": "T",
        "lower": "t",
        "cyrillic": "Т т",
        "ipa": "[t]",
        "desc": "Глухой переднеязычный смычный согласный.",
        "cyr_keys": ["т"],
    },
    {
        "id": "t-caron",
        "letter": "Ť ť",
        "upper": "Ť",
        "lower": "ť",
        "cyrillic": "ТӀ тӀ",
        "ipa": "[tʼ]",
        "desc": "Эйективный (абруптивный) переднеязычный смычный согласный.",
        "cyr_keys": ["тӀ"],
    },
    {
        "id": "u",
        "letter": "U u",
        "upper": "U",
        "lower": "u",
        "cyrillic": "У у",
        "ipa": "[u]",
        "desc": "Огубленный гласный заднего ряда верхнего подъёма.",
        "cyr_keys": ["у"],
    },
    {
        "id": "v",
        "letter": "V v",
        "upper": "V",
        "lower": "v",
        "cyrillic": "В в",
        "ipa": "[v]",
        "desc": "Звонкий губной согласный. Классный показатель мужского рода и заимствования. Правило орфографии: пишется в начале слова перед гласной (vačine, vasasul, vagon, vababay), а также на конце слова или перед согласными (dov).",
        "cyr_keys": ["в"],
        "vw_filter": "v",
    },
    {
        "id": "w",
        "letter": "W w",
        "upper": "W",
        "lower": "w",
        "cyrillic": "В в",
        "ipa": "[w]",
        "desc": "Лабиализация и полугласный [w]. Правило орфографии: пишется после согласных перед гласными (kwine, kwanaze, swine) и в интервокальной позиции перед гласной (kawu, kļawu).",
        "cyr_keys": ["в"],
        "vw_filter": "w",
    },
    {
        "id": "x",
        "letter": "X x",
        "upper": "X",
        "lower": "x",
        "cyrillic": "Х х",
        "ipa": "[χ]",
        "desc": "Глухой увулярный щелевой согласный (фрикатив).",
        "cyr_keys": ["х"],
    },
    {
        "id": "xh",
        "letter": "Xh xh",
        "upper": "Xh",
        "lower": "xh",
        "cyrillic": "Хь хь",
        "ipa": "[x]",
        "desc": "Глухой заднеязычный щелевой согласный (фрикатив).",
        "cyr_keys": ["хь"],
    },
    {
        "id": "kh",
        "letter": "Kh kh",
        "upper": "Kh",
        "lower": "kh",
        "cyrillic": "Хъ хъ",
        "ipa": "[q]",
        "desc": "Глухой увулярный смычный согласный (интенсивный придыхательный).",
        "cyr_keys": ["хъ"],
    },
    {
        "id": "y",
        "letter": "Y y",
        "upper": "Y",
        "lower": "y",
        "cyrillic": "Й й (также в я, ю)",
        "ipa": "[j]",
        "desc": "Палатальный аппроксимант (полугласный). Служит также основой для йотированных гласных: ya (я), yu (ю).",
        "cyr_keys": ["й", "я", "ю"],
    },
    {
        "id": "z",
        "letter": "Z z",
        "upper": "Z",
        "lower": "z",
        "cyrillic": "З з",
        "ipa": "[z]",
        "desc": "Звонкий переднеязычный свистящий согласный.",
        "cyr_keys": ["з"],
    },
    {
        "id": "apostrophe",
        "letter": "'",
        "upper": "'",
        "lower": "'",
        "cyrillic": "Ъ ъ",
        "ipa": "[ʔ]",
        "desc": "Апостроф передаёт гортанную смычку (глоттальный взрыв / хамзу), разделяя слоги и гласные звуки (ma'na, ba'al).",
        "cyr_keys": ["ъ"],
    },
]

# Canonical words: always transliterated dynamically via translit_text()
CANONICAL_WORDS = {
    "v": [
        ("вачӀине", "прийти (о мужчине)"),
        ("васасул", "мальчика, сына (родит. падеж)"),
        ("вагон", "вагон"),
        ("дов", "тот, он (муж. род)"),
        ("вабабай", "ой-ой-ой! (восклицание)"),
    ],
    "w": [
        ("кваназе", "кушать, есть"),
        ("квине", "съесть"),
        ("свине", "погаснуть, потухнуть"),
        ("суне", "погаснуть, потухнуть (альтернативное произношение)"),
        ("каву", "ворота"),
        ("кьаву", "ржавчина"),
    ],
    "l-stroke": [
        ("лӏугӏизе", "кончиться, закончиться"),
        ("ролӏ", "пшеница"),
        ("лӏутӏ", "клин, клинышек"),
    ],
    "apostrophe": [
        ("гьуърул", "легкие (анат.)"),
        ("объём", "объём"),
        ("самаъ", "небо"),
        ("муъминчи", "верующий, уверовавший"),
    ],
    "o-umlaut": [
        ("актёр", "актёр"),
        ("зачёт", "зачёт"),
        ("маёвка", "маёвка"),
    ],
}

# Canonical phrases: always transliterated dynamically via translit_text()
CANONICAL_PHRASES = {
    "v": [
        ("Дов васасул эмен вуго.", "Он отец мальчика."),
        ("ВачӀа нижер росулъе!", "Приходи в наше село!"),
        ("Вагон шагьаралде щвана.", "Вагон прибыл в город."),
    ],
    "w": [
        ("Кваназе гӀодов чӀа.", "Садись кушать."),
        ("маххул каву", "железные ворота"),
        ("ЦӀа свине гьабуна.", "Огонь потушили."),
    ],
    "l-stroke": [
        ("цӏулал лӏутӏ", "деревянный клин"),
        ("гӏарац лӏугӏана", "деньги кончились"),
        ("тушманасул гуллица досул керен борлӏун букӏана", "вражеская пуля пробила ему грудь"),
    ],
    "apostrophe": [
        ("Вабаъ щваги дуде!", "Да заразит тебя холера!"),
        ("буъбуиялда кӏалъазе", "бурчать"),
        ("диирго йокьулелъе санаъ гьабизин", "воздам я хвалу возлюбленной своей"),
    ],
    "o-umlaut": [
        ("Зачёт лъезе.", "Поставить зачёт."),
        ("Зачёт кьезе.", "Сдать зачёт."),
        ("Дица зачёт кьуна.", "Я сдал зачёт."),
    ],
}


def clean_gloss(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    parts = [p.strip() for p in text.split(";") if p.strip()]
    if len(parts) > 2:
        text = "; ".join(parts[:2])
    if len(text) > 65:
        text = text[:62] + "..."
    return text


def collect_from_jsonl():
    if not SOURCE.exists():
        print(f"Warning: {SOURCE} does not exist, skipping JSONL scan.")
        return {}, {}, {}

    candidates_by_key = {}
    phrases_by_first_key = {}
    phrases_by_any_key = {}

    print(f"Reading {SOURCE}...")
    with SOURCE.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line)
            word = norm(d.get("word", "").strip())
            senses = d.get("senses") or []
            gloss = clean_gloss(senses[0].get("text", "")) if senses else ""

            # Check headword
            tokens = tokenize(word) if word else []
            first_key = tokens[0][1] if tokens else None

            if word and 2 <= len(word) <= 14 and gloss and "-" not in word and first_key:
                if first_key not in candidates_by_key:
                    candidates_by_key[first_key] = []
                candidates_by_key[first_key].append((word, gloss))

            # Check phrases
            for sense in senses:
                for ex in sense.get("examples") or []:
                    av = norm((ex.get("av") or "").strip())
                    ru = clean_gloss((ex.get("ru") or "").strip())
                    if not av or not ru or " " not in av:
                        continue
                    if len(av) < 10 or len(av) > 60:
                        continue

                    if first_key:
                        if first_key not in phrases_by_first_key:
                            phrases_by_first_key[first_key] = []
                        if len(phrases_by_first_key[first_key]) < 20:
                            phrases_by_first_key[first_key].append((av, ru))

                    for _, key in tokenize(av):
                        if key not in phrases_by_any_key:
                            phrases_by_any_key[key] = []
                        if len(phrases_by_any_key[key]) < 20:
                            phrases_by_any_key[key].append((av, ru))

    return candidates_by_key, phrases_by_first_key, phrases_by_any_key


def main():
    candidates_by_key, phrases_by_first_key, phrases_by_any_key = collect_from_jsonl()

    alphabet_data = []

    for item in LATIN_LETTERS:
        letter_id = item["id"]
        cyr_keys = [norm(k) for k in item["cyr_keys"]]
        vw_filter = item.get("vw_filter")

        # 1. Collect Words
        words = []
        if letter_id in CANONICAL_WORDS:
            for cyr, ru in CANONICAL_WORDS[letter_id]:
                words.append({"cyrillic": cyr, "latin": translit_text(cyr), "ru": ru})
        else:
            seen_words = set()
            for key in cyr_keys:
                pool = candidates_by_key.get(key, [])
                for cyr, ru in pool:
                    if cyr in seen_words:
                        continue
                    lat = translit_text(cyr)
                    if vw_filter == "v" and "v" not in lat.lower():
                        continue
                    if vw_filter == "w" and "w" not in lat.lower():
                        continue
                    seen_words.add(cyr)
                    words.append({"cyrillic": cyr, "latin": lat, "ru": ru})
                    if len(words) >= 4:
                        break
                if len(words) >= 4:
                    break

        # 2. Collect Phrases
        phrases = []
        if letter_id in CANONICAL_PHRASES:
            for cyr, ru in CANONICAL_PHRASES[letter_id]:
                phrases.append({"cyrillic": cyr, "latin": translit_text(cyr), "ru": ru})
        else:
            seen_phrases = set()
            # First preference: phrases from headwords starting with this letter
            for key in cyr_keys:
                pool = phrases_by_first_key.get(key, [])
                for cyr, ru in pool:
                    if cyr in seen_phrases:
                        continue
                    lat = translit_text(cyr)
                    if vw_filter == "v" and "v" not in lat.lower():
                        continue
                    if vw_filter == "w" and "w" not in lat.lower():
                        continue
                    seen_phrases.add(cyr)
                    phrases.append({"cyrillic": cyr, "latin": lat, "ru": ru})
                    if len(phrases) >= 3:
                        break
                if len(phrases) >= 3:
                    break

            # Fallback: phrases containing this letter anywhere
            if len(phrases) < 3:
                for key in cyr_keys:
                    pool = phrases_by_any_key.get(key, [])
                    for cyr, ru in pool:
                        if cyr in seen_phrases:
                            continue
                        lat = translit_text(cyr)
                        if vw_filter == "v" and "v" not in lat.lower():
                            continue
                        if vw_filter == "w" and "w" not in lat.lower():
                            continue
                        seen_phrases.add(cyr)
                        phrases.append({"cyrillic": cyr, "latin": lat, "ru": ru})
                        if len(phrases) >= 3:
                            break
                    if len(phrases) >= 3:
                        break

        entry = {
            "id": item["id"],
            "letter": item["letter"],
            "upper": item["upper"],
            "lower": item["lower"],
            "cyrillic": item["cyrillic"],
            "ipa": item["ipa"],
            "desc": item["desc"],
            "words": words,
            "phrases": phrases,
        }
        alphabet_data.append(entry)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(alphabet_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {OUTPUT} with {len(alphabet_data)} letters.")


if __name__ == "__main__":
    main()
