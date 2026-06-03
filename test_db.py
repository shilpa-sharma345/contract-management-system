# test_db.py

import asyncio
from app.db.db import engine

async def test():
    try:
        async with engine.begin() as conn:
            print("Database Connected Successfully!")
    except Exception as e:
        print("Connection Failed")
        print(e)

asyncio.run(test())