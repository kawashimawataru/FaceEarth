"""tiles_candidate.json のタイルを EOX から丁寧にダウンロードして data/tiles/ にキャッシュする。

- 並列 6 接続・指数バックオフでリトライ
- 既存ファイルはスキップ (再実行は無料)
"""

import asyncio
import json
import sys

import httpx

from config import CACHE, CANDIDATES_JSON, TILE_URL_TEMPLATE

CONCURRENCY = 6
HEADERS = {"User-Agent": "FaceEarth-pipeline/1.0 (art project; contact via github)"}


def tile_path(z: int, x: int, y: int):
    return CACHE / str(z) / str(x) / f"{y}.jpg"


async def fetch_one(client: httpx.AsyncClient, sem: asyncio.Semaphore, t: dict) -> bool:
    path = tile_path(t["z"], t["x"], t["y"])
    if path.exists():
        return True
    url = TILE_URL_TEMPLATE.format(z=t["z"], x=t["x"], y=t["y"])
    async with sem:
        for attempt in range(4):
            try:
                r = await client.get(url)
                if r.status_code == 200:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(r.content)
                    return True
                if r.status_code == 404:
                    return False
            except httpx.HTTPError:
                pass
            await asyncio.sleep(1.5 * 2**attempt)
    print(f"FAILED {url}", file=sys.stderr)
    return False


async def main() -> None:
    tiles = json.loads(CANDIDATES_JSON.read_text())
    sem = asyncio.Semaphore(CONCURRENCY)
    done = 0
    async with httpx.AsyncClient(headers=HEADERS, timeout=30) as client:
        tasks = [fetch_one(client, sem, t) for t in tiles]
        for i, coro in enumerate(asyncio.as_completed(tasks), 1):
            await coro
            done += 1
            if done % 200 == 0 or done == len(tiles):
                print(f"downloaded {done}/{len(tiles)}")
    print("done")


if __name__ == "__main__":
    asyncio.run(main())
