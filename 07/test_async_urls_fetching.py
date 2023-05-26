import unittest
import tempfile
from unittest.mock import MagicMock
from unittest.mock import patch
from async_urls_fetching import fetch_url, process_urls, read_urls_async


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

    async def test_read_urls_async(self):
        expected = ['https://www.example1.com', 'https://www.example2.com']
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            file.write('\n'.join(expected))

        result = [line async for line in read_urls_async(file.name)]
        self.assertEqual(result, expected)

    async def test_process_urls(self):
        urls = ['https://www.example1.com', 'https://www.example2.com', 'https://www.example3.com']

        async def mock_fetch_url(session, url):
            return {url: 'response'}

        async def mock_read_urls_async(url_file_path):
            for elem in urls:
                yield elem

        with patch('async_urls_fetching.fetch_url', side_effect=mock_fetch_url):
            with patch('async_urls_fetching.read_urls_async', side_effect=mock_read_urls_async):
                result = await process_urls(3, '/file')
                self.assertEqual(result, [{'https://www.example1.com': 'response'},
                                          {'https://www.example2.com': 'response'},
                                          {'https://www.example3.com': 'response'}])

    async def test_no_file(self):
        url_file_path = 'ogfdjkjhdf'

        with self.assertRaises(FileNotFoundError) as err:
            result = [line async for line in read_urls_async(url_file_path)]

        with self.assertRaises(FileNotFoundError) as err:
            result = await process_urls(3, url_file_path)

    async def test_empty_file(self):
        concurrency = 2
        urls = []

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            pass

        result = [line async for line in read_urls_async(file.name)]
        self.assertEqual(result, urls)

        result = await process_urls(concurrency, file.name)
        self.assertEqual(result, urls)

    async def test_function_errors(self):
        concurrency = 2
        urls = 'urls.txt'

        with patch('async_urls_fetching.fetch_url', side_effect=Exception):
            with self.assertRaises(Exception) as err:
                result = await process_urls(concurrency, urls)

        with patch('async_urls_fetching.read_urls_async', side_effect=Exception):
            with self.assertRaises(Exception) as err:
                result = await process_urls(concurrency, urls)


if __name__ == '__main__':
    unittest.main()
