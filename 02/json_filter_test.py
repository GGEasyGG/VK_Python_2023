import unittest
import random
import json
from unittest import mock
from faker import Faker
from json_filter import parse_json


class TestParseJson(unittest.TestCase):
    def setUp(self):
        self.fake = Faker(locale='Ru_ru')

        num_fields = random.randint(1, 10)

        data = {}
        for _ in range(num_fields):
            key = self.fake.word()
            value = self.fake.sentence()[:-1].lower()
            data[key] = value

        self.json_string = json.dumps(data, ensure_ascii=False)

        max_count = max([len(elem.split(' ')) for elem in data.values()])

        self.keywords_random = [self.fake.word() for _ in range(random.randint(1, max_count))]
        self.required_fields_random = [self.fake.word() for _ in range(random.randint(1, len(data)))]

        keywords = set()
        self.required_fields = list(data.keys())[0:random.randint(1, 5)]

        self.length = 0
        for elem in self.required_fields[0:random.randint(1, len(self.required_fields))]:
            keywords.update(data[elem].split(' ')[0:random.randint(1, max_count)])

        self.keywords = list(keywords)

        for elem in self.required_fields:
            for element in self.keywords:
                if element in data[elem].split(' '):
                    self.length += 1

    def test_parse_json(self):
        with mock.patch('json_filter.keyword_callback') as func:
            for i in range(1, 101):
                parse_json(self.json_string, func, required_fields=self.required_fields,
                           keywords=self.keywords)
                self.assertEqual(func.call_count, i * self.length)

    def test_parse_json_with_some_same_words_in_different_fields(self):
        with mock.patch('json_filter.keyword_callback') as func:
            parse_json('{"key1": "word1 word2", "key2": "word2 word3", "key3": "word1 word3"}', func,
                       required_fields=["key1", "key2", "key3"], keywords=["word2", "word1"])
            self.assertEqual(func.call_count, 4)

            parse_json('{"key1": "word1 word2", "key2": "word2 word3", "key3": "word1 word3"}', func,
                       required_fields=["key1", "key2"], keywords=["word2", "word1"])
            self.assertEqual(func.call_count, 4 + 3)

            parse_json('{"key1": "word1 word2", "key2": "word2 word3", "key3": "word1 word3"}', func,
                       required_fields=["key1", "key3"], keywords=["word2", "word1"])
            self.assertEqual(func.call_count, 7 + 3)

    def test_parse_json_keyword_callback_parameters(self):
        with mock.patch('json_filter.keyword_callback') as func:
            parse_json(self.json_string, func, required_fields=self.required_fields,
                       keywords=self.keywords)

            calls = []
            for elem in self.required_fields:
                for element in self.keywords:
                    if element in json.loads(self.json_string)[elem].split(' '):
                        calls.append(mock.call(element, elem))

            self.assertEqual(func.mock_calls, calls)

    def test_parse_json_with_keyword_callback_named_parameters(self):
        with mock.patch('json_filter.keyword_callback') as func:
            parse_json(self.json_string, func, required_fields=self.required_fields,
                       keywords=self.keywords)
            self.assertEqual(func.call_count, self.length)

            parse_json(self.json_string, func, self.required_fields, self.keywords)
            self.assertEqual(func.call_count, 2 * self.length)

            parse_json(self.json_string, func, keywords=self.keywords, required_fields=self.required_fields)
            self.assertEqual(func.call_count, 3 * self.length)

    def test_parse_json_with_empty_named_parameters(self):
        with mock.patch('json_filter.keyword_callback') as func:
            parse_json(self.json_string, func, required_fields=self.required_fields, keywords=[])
            self.assertEqual(func.call_count, 0)

            parse_json(self.json_string, func, required_fields=[], keywords=self.keywords)
            self.assertEqual(func.call_count, 0)

    def test_parse_json_with_empty_json_string(self):
        with mock.patch('json_filter.keyword_callback') as func:
            parse_json('{}', func, required_fields=self.required_fields, keywords=self.keywords)
            self.assertEqual(func.call_count, 0)

    def test_parse_json_with_keyword_callback_not_callback(self):
        with mock.patch('json_filter.keyword_callback') as func:
            parse_json(self.json_string, func, required_fields=self.required_fields_random,
                       keywords=self.keywords_random)
            self.assertEqual(func.call_count, 0)

    def test_parse_json_with_none_parameters(self):
        with mock.patch('json_filter.keyword_callback') as func:
            parse_json(self.json_string, func, required_fields=self.required_fields_random)
            self.assertEqual(func.call_count, 0)

            parse_json(self.json_string, func, keywords=self.keywords_random)
            self.assertEqual(func.call_count, 0)

            parse_json(self.json_string, func)
            self.assertEqual(func.call_count, 0)

    def test_parse_json_with_wrong_params(self):
        with mock.patch('json_filter.keyword_callback') as func:
            with self.assertRaises(TypeError):
                parse_json(123, func, required_fields=['a', 'b', 'c'], keywords=['a', 'b', 'c'])

            with self.assertRaises(TypeError):
                parse_json(self.json_string, 123, required_fields=['a', 'b', 'c'], keywords=['a', 'b', 'c'])

            with self.assertRaises(TypeError):
                parse_json(self.json_string, func, required_fields=123, keywords=['a', 'b', 'c'])

            with self.assertRaises(TypeError):
                parse_json(self.json_string, func, required_fields=['a', 'b', 'c'], keywords=123)

    def test_parse_json_with_non_valid_json_str(self):
        with mock.patch('json_filter.keyword_callback') as func:
            with self.assertRaises(ValueError):
                parse_json('fadjj jfadh hafjkhds hafjgfhjd', func, required_fields=['a', 'b', 'c'],
                           keywords=['a', 'b', 'c'])

            with self.assertRaises(ValueError):
                parse_json('{"fadjj": "jfadh hafjkhds hafjgfhjd", "fjsfhdgsh"}', func, required_fields=['a', 'b', 'c'],
                           keywords=['a', 'b', 'c'])

    def test_parse_json_with_keyword_callback_error(self):
        with mock.patch('json_filter.keyword_callback') as func:
            func.side_effect = Exception
            with self.assertRaises(Exception):
                parse_json(self.json_string, func, required_fields=self.required_fields,
                           keywords=self.keywords)

    def test_parse_json_with_non_primitive_json_str(self):
        with mock.patch('json_filter.keyword_callback') as func:
            with self.assertRaises(ValueError) as err:
                parse_json('{"fadjj": ["jfadh", "hafjkhds", "hafjgfhjd"]}', func, required_fields=['a', 'b', 'c'],
                           keywords=['a', 'b', 'c'])

            self.assertEqual(str(err.exception), "This is non primitive json string")

            with self.assertRaises(ValueError) as err:
                parse_json('{"fadjj": "jfadh hafjkhds hafjgfhjd", "fjdhjs": {"dhsj": "fjdsk fsvjh sf  sfdf"}}',
                           func, required_fields=['a', 'b', 'c'], keywords=['a', 'b', 'c'])

            self.assertEqual(str(err.exception), "This is non primitive json string")

    def test_with_non_string_keywords_or_required_fields(self):
        with mock.patch('json_filter.keyword_callback') as func:
            with self.assertRaises(TypeError):
                parse_json(self.json_string, func, required_fields=[1, "df", 3], keywords=['a', 'b', 'c'])

            with self.assertRaises(TypeError):
                parse_json(self.json_string, func, required_fields=['a', 'b', 'c'], keywords=["hf", 2, 3])
