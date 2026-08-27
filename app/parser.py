import httpx
from bs4 import BeautifulSoup

from app.core.settings import settings
from app.core.utils import load_page_urls
from app.database.connection import get_connection
from app.services import ImageService


class Parser:

    def __init__(self):
        self.conn = get_connection()
        self.img_service = ImageService(next(self.conn))
        self.page_urls = load_page_urls(settings.urls_file_path)

    def run_parser(self):

        for page_url in self.page_urls:
            print(f"Parsing page: {page_url} ...")

            image_urls = self._parse_image_urls(page_url)

            print(f"Getting images:")

            images, skipped = self.img_service.get_images(image_urls)

            if skipped:
                print("Skipped: ", *skipped, sep="\n")

            yield images

    def _parse_image_urls(self, url: str) -> list[str]:

        response = httpx.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        urls = []

        for img in soup.find_all("a", class_="rel-link"):
            img_url = img.get("href")

            if img_url:
                urls.append(img_url)

        return urls
