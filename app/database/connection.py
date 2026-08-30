from typing import Any, AsyncGenerator

import aiosqlite


async def get_connection() -> AsyncGenerator[aiosqlite.Connection, Any]:
    async with aiosqlite.connect("app/database/parser.db") as conn:
        yield conn
