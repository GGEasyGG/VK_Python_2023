import time
import asyncio
import argparse
import aiohttp
import aiofiles


async def fetch_url(session, url):
    async with session.get(url) as response:
        return {url: await response.text()}


async def read_urls_async(url_file_path):
    async with aiofiles.open(url_file_path, mode='r') as file:
        async for line in file:
            yield line.strip()


async def process_urls(concurrency, url_file_path):
    results = []

    async def worker():
        async with aiohttp.ClientSession() as session:
            while True:
                url = await get_next_url()
                if url is None:
                    break
                result = await fetch_url(session, url)
                results.append(result)

    async def get_next_url():
        async with lock:
            try:
                url = await url_iterator.__anext__()
            except StopAsyncIteration:
                url = None
            return url

    lock = asyncio.Lock()

    url_iterator = read_urls_async(url_file_path)

    worker_tasks = []
    for _ in range(concurrency):
        task = asyncio.create_task(worker())
        worker_tasks.append(task)

    await asyncio.gather(*worker_tasks)

    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('concurrency', type=int)
    parser.add_argument('url_file', type=str)
    args = parser.parse_args()

    start = time.time()
    final_result = asyncio.run(process_urls(args.concurrency, args.url_file))
    end = time.time()

    total_time = end - start
    print(f'Execution time: {round(total_time, 3)} seconds')

    print(*final_result, sep='\n\n')
