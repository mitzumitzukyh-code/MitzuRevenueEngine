import asyncio
from app.db import init_db
from app.services.scout_runner import ScoutRunner

async def main():
    init_db()
    await ScoutRunner().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
