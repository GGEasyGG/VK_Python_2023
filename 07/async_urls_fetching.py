import time
import asyncio
import aiohttp
import aiofiles
import argparse


async def fetch_url(session, url):
    async with session.get(url) as response:
        return {url: await response.text()}


async def fetch_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch_url(session, url)) for url in urls]
        batch_results = await asyncio.gather(*tasks)
        return batch_results


async def read_urls_async(url_file_path):
    async with aiofiles.open(url_file_path, mode='r') as file:
        async for line in file:
            yield line.strip()


async def run_batches(concurrency, url_file_path):
    results = []

    async for batch in batch_urls(read_urls_async(url_file_path), concurrency):
        batch_results = await fetch_urls(batch)
        results.extend(batch_results)

    return results


async def batch_urls(urls, batch_size):
    batch = []
    async for url in urls:
        batch.append(url)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if len(batch) > 0:
        yield batch


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('concurrency', type=int)
    parser.add_argument('url_file', type=str)
    args = parser.parse_args()

    start = time.time()
    result = asyncio.run(run_batches(args.concurrency, args.url_file))
    end = time.time()

    total_time = end - start
    print(f'Execution time: {round(total_time, 3)} seconds')

    print(*result, sep='\n\n')
