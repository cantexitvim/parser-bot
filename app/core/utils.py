from typing import Iterator


class ProgressBar:

    def __init__(self, total: int, fill: str = "█", length: int = 50):
        self.total = total
        self.progress = 0
        self.fill = fill
        self.length = length

    def show(self):
        self.progress += 1

        percent = round(self.progress * 100 / self.total, 2)
        filled_length = int(self.progress * self.length // self.total)
        bar = self.fill * filled_length + "-" * (self.length - filled_length)

        print(
            f"\rProgress | {bar} | {percent}% | {self.progress}/{self.total} Complete",
            end="\r",
        )

        if self.progress == self.total:
            print()


def load_page_urls(path: str) -> Iterator[str]:
    with open(path, "r", encoding="utf-8") as urls:
        for raw_url in urls:
            url = raw_url.strip()

            if not url:
                continue

            yield url
