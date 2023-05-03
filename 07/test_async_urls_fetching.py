import unittest
import tempfile
import aiohttp
from unittest.mock import MagicMock, Mock, call
from unittest.mock import patch
from async_urls_fetching import fetch_url, fetch_urls, read_urls_async, batch_urls, run_batches


class TestAsyncFunctions(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_url(self):
        async def text(string):
            return string

        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.text.return_value = text('mocked response')
        mock_session.get.return_value.__aenter__.return_value = mock_response
        url = 'https://www.example.com'
        expected = {'https://www.example.com': 'mocked response'}
        result = await fetch_url(mock_session, url)
        self.assertEqual(result, expected)

    async def test_fetch_urls(self):
        urls = ['https://www.example1.com', 'https://www.example2.com']
        expected = [{'https://www.example1.com': 'mocked response 1'},
                    {'https://www.example2.com': 'mocked response 2'}]

        async def mock_fetch_url(session, url):
            return {url: 'mocked response ' + url[-5]}

        func = Mock(side_effect=mock_fetch_url)

        with patch('async_urls_fetching.fetch_url', func):
            result = await fetch_urls(urls)
            self.assertEqual(result, expected)

        self.assertEqual([(str(aiohttp.ClientSession), 'https://www.example1.com'),
                          (str(aiohttp.ClientSession), 'https://www.example2.com')],
                         [(str(type(elem.args[0])), elem.args[1]) for elem in func.call_args_list])

    async def test_read_urls_async(self):
        expected = ['https://www.example1.com', 'https://www.example2.com']
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            file.write('\n'.join(expected))

        result = [line async for line in read_urls_async(file.name)]
        self.assertEqual(result, expected)

    async def test_batch_urls(self):
        urls = ['https://www.example1.com', 'https://www.example2.com', 'https://www.example3.com']
        batch_size = 2
        expected = [['https://www.example1.com', 'https://www.example2.com'], ['https://www.example3.com']]

        async def mock_read_urls_async(url_file_path):
            for elem in urls:
                yield elem

        with patch('async_urls_fetching.read_urls_async', mock_read_urls_async):
            result = [batch async for batch in batch_urls(mock_read_urls_async('urls.txt'), batch_size)]
            self.assertEqual(result, expected)

    async def test_run_batches(self):
        concurrency = 2

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            pass

        expected = [{'https://www.example1.com': 'mocked response 1'},
                    {'https://www.example2.com': 'mocked response 2'},
                    {'https://www.example3.com': 'mocked response 3'},
                    {'https://www.example4.com': 'mocked response 4'}]

        async def mock_batch_urls(urls, batch_size):
            url = [['https://www.example1.com', 'https://www.example2.com'],
                   ['https://www.example3.com', 'https://www.example4.com']]

            for elem in url:
                yield elem

        async def mock_fetch_urls(batch):
            res = []

            for elem in batch:
                res.append({elem: 'mocked response ' + elem[-5]})

            return res

        async def mock_read_urls_async(urls_file_path):
            url = ['https://www.example1.com', 'https://www.example2.com',
                   'https://www.example3.com', 'https://www.example4.com']

            for elem in url:
                yield elem

        fun1 = Mock(side_effect=mock_batch_urls)
        fun2 = Mock(side_effect=mock_fetch_urls)
        fun3 = Mock(side_effect=mock_read_urls_async)

        with patch('async_urls_fetching.batch_urls', fun1), \
             patch('async_urls_fetching.fetch_urls', fun2), \
             patch('async_urls_fetching.read_urls_async', fun3):
            result = await run_batches(concurrency, file.name)
            self.assertEqual(result, expected)

        self.assertEqual([("<class 'async_generator'>", 2)],
                         [(str(type(elem.args[0])), elem.args[1]) for elem in fun1.call_args_list])

        self.assertEqual([call(['https://www.example1.com', 'https://www.example2.com']),
                          call(['https://www.example3.com', 'https://www.example4.com'])],
                         fun2.call_args_list)

        self.assertEqual([call(file.name)], fun3.call_args_list)

    async def test_no_file(self):
        url_file_path = 'ogfdjkjhdf'

        with self.assertRaises(FileNotFoundError) as err:
            result = [line async for line in read_urls_async(url_file_path)]

        with self.assertRaises(FileNotFoundError) as err:
            result = await run_batches(2, url_file_path)

    async def test_empty_file(self):
        concurrency = 2
        urls = []

        async def mock_fetch_url(session, url):
            return {url: 'mocked response ' + url[-5]}

        with patch('async_urls_fetching.fetch_url', mock_fetch_url):
            result = await fetch_urls(urls)
            self.assertEqual(result, urls)

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            pass

        result = [line async for line in read_urls_async(file.name)]
        self.assertEqual(result, urls)

        result = [batch async for batch in batch_urls(read_urls_async(file.name), concurrency)]
        self.assertEqual(result, urls)

        result = await run_batches(concurrency, file.name)
        self.assertEqual(result, urls)

    async def test_batch_size_gt_file_lines_count(self):
        urls = ['https://www.example1.com', 'https://www.example2.com', 'https://www.example3.com']
        batch_size = 6
        expected = [['https://www.example1.com', 'https://www.example2.com', 'https://www.example3.com']]

        async def mock_read_urls_async(url_file_path):
            for elem in urls:
                yield elem

        with patch('async_urls_fetching.read_urls_async', mock_read_urls_async):
            result = [batch async for batch in batch_urls(mock_read_urls_async('urls.txt'), batch_size)]
            self.assertEqual(result, expected)

    async def test_function_errors(self):
        concurrency = 2
        urls = 'urls.txt'

        with patch('async_urls_fetching.fetch_url', side_effect=Exception):
            with self.assertRaises(Exception) as err:
                result = await fetch_urls(urls)

        with patch('async_urls_fetching.fetch_urls', side_effect=Exception):
            with self.assertRaises(Exception) as err:
                result = await run_batches(concurrency, urls)

        with patch('async_urls_fetching.read_urls_async', side_effect=Exception):
            with self.assertRaises(Exception) as err:
                result = await run_batches(concurrency, urls)

        with patch('async_urls_fetching.batch_urls', side_effect=Exception):
            with self.assertRaises(Exception) as err:
                result = await run_batches(concurrency, urls)


if __name__ == '__main__':
    unittest.main()
