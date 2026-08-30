from datetime import datetime
from urllib.parse import urljoin

import httpx
from aiogram import Bot
from bs4 import BeautifulSoup

from app.core.settings import settings
from app.database.connection import get_connection
from app.services.images import ImageService
from app.utils.load import load_domains, load_page_urls
from app.utils.request import get_with_retry
from app.utils.telegram import send_images


class Parser:
    async def init(self, bot: Bot):
        self.bot = bot

        self.client = httpx.AsyncClient(headers={"User-Agent": "ParserBot/1.0"})
        self.conn = get_connection()

        self.img_service = ImageService(conn=await anext(self.conn), client=self.client)

        self.page_urls = load_page_urls(settings.page_urls_path)
        self.domains = load_domains(settings.domains_path)
        self.settings = settings

    async def run_parser(self) -> None:
        print("Running parser...")

        for row in self.page_urls:
            page_url, *tag = row.split()

            hashtag = "".join(tag) if tag else settings.default_hashtag

            print(f"Parsing page: {page_url} ...")

            image_urls = await self._parse_image_urls(page_url)

            if not image_urls:
                print(f"Skipped url: {page_url}\n")
                continue

            print("Getting images:")

            images, skipped = await self.img_service.get_images(image_urls)

            if skipped:
                print(
                    f"Skipped urls writed to file: {self.settings.skipped_urls_path}\n"
                )
                self.write_skipped_log(self.settings.skipped_urls_path, skipped)

            if images:
                await send_images(bot=self.bot, images=images, hashtag=hashtag)

                await self.img_service.save_images()
            else:
                print("Nothing to send\n")
                continue

    async def _parse_image_urls(self, url: str) -> list[str] | None:
        try:
            response = await get_with_retry(client=self.client, url=url)
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error occured when parsing page url. Detail: {str(e)}")
            return None

        if response is None:
            print()

        params = self._get_domain_params(url)

        if params is None or "tag" not in params:
            print(f"Invalid domain params or unknown domain in the url: {url}")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        urls = []

        if "class" not in params:
            images = soup.find_all(params["tag"])
        else:
            images = soup.find_all(params["tag"], class_=params["class"])

        for img in images:
            img_url = img.get(params["attribute"])

            if img_url:
                abs_url = urljoin(url, img_url)

                urls.append(abs_url)

        return urls

    def _get_domain_params(self, url: str) -> dict | None:
        ind = url.find("//") + 2

        domain = url[ind : url.find("/", ind)]

        params = self.domains.get(domain)

        return params

    def write_skipped_log(self, path: str, skipped: dict) -> None:
        timestamp = datetime.now().replace(microsecond=0)

        with open(path, "a", encoding="utf-8") as outp:
            outp.write(f"\n-------{timestamp}-------\n")

            for url, details in skipped.items():
                outp.write(f"\nSkipped: {url}\nDetails: {details}\n")


parser = Parser()
