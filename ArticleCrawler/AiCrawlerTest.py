import asyncio
from crawl4ai import AsyncWebCrawler
import json


async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url="https://www.planetf1.com/news/alleged-evidence-tyre-cooling-trick-red-bull-accusation")
        print(result.json)
        loads = json.loads(result.json)
        print(loads)

if __name__ == "__main__":
    asyncio.run(main())

