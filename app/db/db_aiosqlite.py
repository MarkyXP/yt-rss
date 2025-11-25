import aiosqlite


async def main():
    async with aiosqlite.connect("mydatabase.db") as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)"
        )
        await db.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
        await db.commit()

        cursor = await db.execute("SELECT * FROM users")
        async for row in cursor:
            print(row)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
