import hashlib
from pathlib import PurePosixPath
from urllib.parse import urlparse

from aiosqlite import Connection, IntegrityError
from httpx import AsyncClient

from app.core.exceptions import ImageAlreadyExistsError, UnsupportedImageExtension
from app.database.repositories import get_image_by_hash, get_image_by_url, save_image
from app.utils.progress_bar import ProgressBar
from app.utils.request import get_with_retry


class ImageService:
    def __init__(self, conn: Connection, client: AsyncClient):
        self.conn = conn
        self.client = client
        self.images = {}

    async def get_images(self, urls: list[str]) -> tuple[list, dict]:
        images = []
        skipped = {}

        progress_bar = ProgressBar(len(urls))

        for img_url in urls:
            progress_bar.show()

            try:
                db_image = await get_image_by_url(self.conn, img_url)

                if db_image:
                    raise ImageAlreadyExistsError()

                img_bytes = await self.get_image(img_url)

                ext = self._get_img_ext(img_url)

                images.append((img_bytes, ext))
            except Exception as e:
                skipped[img_url] = str(e)

        return images, skipped

    async def get_image(self, url: str) -> bytes:
        image_response = await get_with_retry(client=self.client, url=url)

        image_bytes = image_response.content

        image_hash = hashlib.sha256(image_bytes).hexdigest()

        img = await get_image_by_hash(self.conn, image_hash)

        if img is not None:
            raise ImageAlreadyExistsError()

        self.images[url] = image_hash

        return image_bytes

    async def save_images(self):
        for url, hash in self.images.items():
            try:
                await save_image(conn=self.conn, url=url, hash=hash)
            except IntegrityError:
                continue

            await self.conn.commit()

    def _get_img_ext(self, url: str) -> str | None:
        path = urlparse(url).path
        ext = PurePosixPath(path).suffix

        if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
            raise UnsupportedImageExtension()

        return ext
