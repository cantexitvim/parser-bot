from datetime import UTC, datetime

from aiosqlite import Connection, Row


async def get_image_by_url(conn: Connection, url: str) -> Row | None:
    result = await conn.execute("SELECT hash FROM images WHERE source_url = ?", (url,))

    return await result.fetchone()


async def get_image_by_hash(conn: Connection, hash: str) -> Row | None:
    result = await conn.execute("SELECT hash FROM images WHERE hash = ?", (hash,))

    return await result.fetchone()


async def save_image(*, conn: Connection, url: str, hash: str) -> None:
    created_at = str(datetime.now(UTC))

    await conn.execute(
        "INSERT INTO images(source_url, hash, created_at) VALUES(?, ?, ?)",
        (url, hash, created_at),
    )
