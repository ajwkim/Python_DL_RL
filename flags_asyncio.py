import time
from pathlib import Path
import asyncio
from httpx import AsyncClient

pop20_cc = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

base_url = 'https://www.fluentpython.com/data/flags'
dest_dir = Path('downloaded')

def save_flag(img, filename):
    (dest_dir / filename).write_bytes(img)

async def get_flag(client: AsyncClient, cc: str) -> bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url, timeout=6.1, follow_redirects=True)
    return resp.read()

async def download_one(client: AsyncClient, cc: str):
    image = await get_flag(client, cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc

async def supervisor(cc_list: list[str]) -> int:
    async with AsyncClient() as client:
        todo = [download_one(client, cc) for cc in sorted(cc_list)]
        res = await asyncio.gather(*todo)
    return len(res)

def download_many(cc_list: list[str]) -> int:
    return asyncio.run(supervisor(cc_list))

def main(downloader):
    dest_dir.mkdir(exist_ok=True)
    t0 = time.perf_counter()
    count = downloader(pop20_cc)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')


if __name__ == '__main__':
    main(download_many)