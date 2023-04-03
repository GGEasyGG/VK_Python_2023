import io
import os
import unittest
import tempfile
from file_generator import search_lines


class TestSearchLines(unittest.TestCase):
    def test_file_name_as_str(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("The quick brown fox\nJumps over the lazy dog\nA rose fell on the paw of Azor\n")

        search_words = ["fox", "rose"]
        result = list(search_lines(f.name, search_words))
        self.assertEqual(result, ["The quick brown fox", "A rose fell on the paw of Azor"])

        search_words = ["paw"]
        result = list(search_lines(f.name, search_words))
        self.assertEqual(result, ["A rose fell on the paw of Azor"])

        os.remove(f.name)

    def test_empty_file(self):
        file = io.StringIO('')
        search_words = ['apple', 'orange', 'banana']
        result = list(search_lines(file, search_words))
        self.assertEqual(result, [])

    def test_no_matches(self):
        file = io.StringIO('This is a test\nof the emergency\nbroadcast system\n')
        search_words = ['apple', 'orange', 'banana']
        result = list(search_lines(file, search_words))
        self.assertEqual(result, [])

    def test_case_insensitivity(self):
        file = io.StringIO('Apples are red\nOranges are orange\nBananas are yellow\n')
        search_words = ['apples', 'OrAnGeS', 'BANANAS']
        result = list(search_lines(file, search_words))
        self.assertEqual(result, ['Apples are red', 'Oranges are orange', 'Bananas are yellow'])

        file = io.StringIO('Apples are red\nOrAnGeS are orange\nBANANAS are yellow\n')
        search_words = ['apples', 'oranges', 'bananas']
        result = list(search_lines(file, search_words))
        self.assertEqual(result, ['Apples are red', 'OrAnGeS are orange', 'BANANAS are yellow'])

    def test_partial_matches(self):
        file = io.StringIO('apple pie\noranges\nbanana bread\n')
        search_words = ['app', 'oran', 'bananas']
        result = list(search_lines(file, search_words))
        self.assertEqual(result, [])

    def test_multiple_matches(self):
        file = io.StringIO('apples are good\nbananas are also good\noranges are not as good\n')
        search_words = ['apples', 'oranges', 'goods']
        result = list(search_lines(file, search_words))
        self.assertEqual(result, ['apples are good', 'oranges are not as good'])

    def test_empty_search_words(self):
        file = io.StringIO('apples are good\nbananas are also good\noranges are not as good\n')
        search_words = []
        results = list(search_lines(file, search_words))
        self.assertEqual(results, [])

    def test_whitespace(self):
        file = io.StringIO('apples    are    good\nbananas    are    also  good\noranges  are   not       as good\n')
        search_words = ['apples', 'bananas', 'oranges']
        results = list(search_lines(file, search_words))
        self.assertEqual(results, ['apples    are    good', 'bananas    are    also  good',
                                   'oranges  are   not       as good'])

    def test_one_search_word_in_every_string(self):
        file = io.StringIO('apples are good\nbananas are also good\noranges are not as good\n')
        search_words = ['good']
        results = list(search_lines(file, search_words))
        self.assertEqual(results, ['apples are good', 'bananas are also good', 'oranges are not as good'])

    def test_duplicate_search_words(self):
        file = io.StringIO('apples are good\nbananas are also good\noranges are not as good\n')
        search_words = ['apples', 'bananas', 'apples']
        results = list(search_lines(file, search_words))
        self.assertEqual(results, ['apples are good', 'bananas are also good'])

    def test_one_string_file(self):
        file = io.StringIO('apples are good bananas are also good oranges are not as good')
        search_words = ['apples', 'bananas', 'oranges']
        results = list(search_lines(file, search_words))
        self.assertEqual(results, ['apples are good bananas are also good oranges are not as good'])

    def test_search_words_with_dashes(self):
        file = io.StringIO("The quick-brown fox\njumps over the lazy-dog")
        search_words = ["quick-brown", "lazy-dog"]
        lines = list(search_lines(file, search_words))
        self.assertEqual(lines, ["The quick-brown fox", "jumps over the lazy-dog"])

    def test_search_words_with_underscores(self):
        file = io.StringIO("The quick_brown fox\njumps over the lazy_dog")
        search_words = ["quick_brown", "lazy_dog"]
        lines = list(search_lines(file, search_words))
        self.assertEqual(lines, ["The quick_brown fox", "jumps over the lazy_dog"])

    def test_file_object_consumption(self):
        file = io.StringIO("The quick brown fox\njumps over the lazy dog")
        search_words = ["quick"]
        with file as f:
            position = f.tell()
            self.assertEqual(position, 0)
            result = list(search_lines(f, search_words))
            self.assertEqual(result, ["The quick brown fox"])
            position = f.tell()
            self.assertEqual(position, len("The quick brown fox\njumps over the lazy dog"))
        self.assertTrue(file.closed)

    def test_invalid_parameters(self):
        file = io.StringIO('apples are good bananas are also good oranges are not as good')
        search_words = 'fjdksjfdg'
        with self.assertRaises(TypeError):
            list(search_lines(file, search_words))

        file.seek(0)
        search_words = [1, (2, 3), 'dsfdgjkf']
        with self.assertRaises(TypeError):
            list(search_lines(file, search_words))

        file = 13234
        search_words = ['apples', 'bananas', 'oranges']
        with self.assertRaises(TypeError):
            list(search_lines(file, search_words))

        file = 'fdksfjjd'
        search_words = ['apples', 'bananas', 'oranges']
        with self.assertRaises(FileNotFoundError):
            list(search_lines(file, search_words))

        file = io.BytesIO(b'fdksfjjd')
        search_words = ['apples', 'bananas', 'oranges']
        with self.assertRaises(TypeError):
            list(search_lines(file, search_words))


if __name__ == '__main__':
    unittest.main()
