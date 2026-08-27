from datetime import UTC, datetime
from sqlite3 import Connection


def get_image_by_url(conn: Connection, url: str) -> tuple | None:
    result = conn.execute("SELECT hash FROM images WHERE source_url = ?", (url,))

    return result.fetchone()


def save_image(*, conn: Connection, url: str, hash: str) -> None:
    created_at = str(datetime.now(UTC))

    conn.execute(
        "INSERT INTO images(source_url, hash, created_at) VALUES(?, ?, ?)",
        (url, hash, created_at),
    )
