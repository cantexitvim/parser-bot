import hashlib
from sqlite3 import Connection, IntegrityError

import httpx

from app.core.utils import ProgressBar
from app.database.repositories import get_image_by_url, save_image


class ImageService:

    def __init__(self, conn: Connection):
        self.conn = conn

    def get_images(self, urls: list[str]) -> tuple[list, list]:
        images = []
        skipped = []

        progress_bar = ProgressBar(len(urls))

        for img_url in urls:
            progress_bar.show()

            image = get_image_by_url(self.conn, img_url)

            if not image:
                img = self.get_image(img_url)

                if img:
                    images.append(img)
                    continue

            skipped.append(img_url)

        return images, skipped

    def get_image(self, url: str) -> bytes | None:
        image_response = httpx.get(url)
        image_response.raise_for_status()

        image_bytes = image_response.content

        image_hash = hashlib.sha256(image_bytes).hexdigest()

        try:
            save_image(conn=self.conn, url=url, hash=image_hash)
        except IntegrityError:
            return None

        self.conn.commit()

        return image_bytes
