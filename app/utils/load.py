import json
from typing import Iterator


def load_page_urls(path: str) -> Iterator[str]:
    with open(path, "r", encoding="utf-8") as urls:
        for raw_url in urls:
            url = raw_url.strip()

            if not url:
                continue

            yield url


def load_domains(path: str) -> dict[str, dict]:
    with open(path, "r", encoding="utf-8") as domains:
        data = json.load(domains)

    return data
