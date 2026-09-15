# alif.avar.me

Аварский алфавит и системы транслитерации:
- **Главная страница (`/`)**: Латинский алфавит (avar.me) с кратким описанием звуков, правилами орфографии (включая различие V и W), примерами слов и аутентичных предложений из словаря.
- **Таблица систем (`/comparison_table.html`)**: Сравнительная таблица различных систем латинизации аварского языка (avar.me, Scientific, 1932, Typing, Forker, Said, Umarilov и др.).
- **Алгоритм транслитерации** — [`transliteration-guide.md`](transliteration-guide.md): формальное описание алгоритма кириллица → avar.me для написания скриптов транслитерации; ссылка на скачивание есть в подвале обеих страниц сайта.

Сайт: <https://alif.avar.me>

## Данные и сборка

- Исходная таблица сравнения — [`data/alphabet.csv`](data/alphabet.csv).
- Данные латинского алфавита с примерами — [`data/alphabet_latin.json`](data/alphabet_latin.json).
- Извлечение примеров из словаря: `python3 build/collect_examples.py`.
- Сборка HTML-страниц:

```bash
python3 build/build.py
```

Локальный просмотр:

```bash
python3 -m http.server 8000
```
