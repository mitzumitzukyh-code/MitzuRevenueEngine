import asyncio
from app.db import init_db
from app.services.market_runner import MarketRunner

async def main():
    init_db()
    await MarketRunner().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
