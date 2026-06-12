from dataclasses import dataclass, field
import json


@dataclass
class SymbolEntry:
    char: str
    keywords: list[str]
    category: str


def load_data(path: str) -> list[SymbolEntry]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    result = []
    for category, symbols in raw.items():
        for char, keywords in symbols.items():
            result.append(SymbolEntry(char=char, keywords=keywords, category=category))
    return result


def filter_symbols(
    data: list[SymbolEntry],
    text: str = "",
    category: str | None = None,
) -> list[SymbolEntry]:
    result = data
    if category:
        result = [e for e in result if e.category == category]
    if text:
        words = [w.strip() for w in text.split() if w.strip()]
        if words:
            for word in words:
                wl = word.lower()
                result = [
                    e
                    for e in result
                    if any(wl in kw.lower() for kw in e.keywords)
                ]
    return result


def get_categories(data: list[SymbolEntry]) -> list[str]:
    seen: list[str] = []
    for e in data:
        if e.category not in seen:
            seen.append(e.category)
    return seen
