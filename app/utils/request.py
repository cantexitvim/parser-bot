import asyncio

from httpx import AsyncClient, ReadTimeout, Response


async def get_with_retry(
    *, client: AsyncClient, url: str, attempts: int = 3, secs: int = 1
) -> Response:
    attempt = 1

    while True:
        try:
            response = await client.get(url)
            response.raise_for_status()

            return response
        except ReadTimeout:
            if attempt == attempts:
                raise

            await asyncio.sleep(secs)

            attempt += 1
