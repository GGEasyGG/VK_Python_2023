import unittest
import time
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_set_and_get(self):
        cache = LRUCache(limit=5)
        cache.set('a', 1)
        cache.set('b', 'abc')
        cache.set('c', [1, 2, 3])
        cache.set('d', (1, 2, 3))
        cache.set('e', {1: 1, 2: 2, 3: 3})
        self.assertEqual(cache.get('a'), 1)
        self.assertEqual(cache.get('b'), 'abc')
        self.assertEqual(cache.get('c'), [1, 2, 3])
        self.assertEqual(cache.get('d'), (1, 2, 3))
        self.assertEqual(cache.get('e'), {1: 1, 2: 2, 3: 3})

    def test_not_int_cache_size(self):
        with self.assertRaises(TypeError) as err:
            cache = LRUCache(5.5)

        self.assertEqual(str(err.exception), "The cache size must be of type int")

        with self.assertRaises(TypeError) as err:
            cache = LRUCache((1, 2))

        self.assertEqual(str(err.exception), "The cache size must be of type int")

        with self.assertRaises(TypeError) as err:
            cache = LRUCache([1, 2])

        self.assertEqual(str(err.exception), "The cache size must be of type int")

        with self.assertRaises(TypeError) as err:
            cache = LRUCache('dksfdgkf')

        self.assertEqual(str(err.exception), "The cache size must be of type int")

        with self.assertRaises(TypeError) as err:
            cache = LRUCache({1: 1, 2: 2})

        self.assertEqual(str(err.exception), "The cache size must be of type int")

    def test_non_positive_cache_size(self):
        with self.assertRaises(ValueError) as err:
            cache = LRUCache(0)

        self.assertEqual(str(err.exception), "The cache cannot be non-positive size")

        with self.assertRaises(ValueError) as err:
            cache = LRUCache(-5)

        self.assertEqual(str(err.exception), "The cache cannot be non-positive size")

    def test_get_nonexistent_key(self):
        cache = LRUCache(limit=3)
        self.assertEqual(cache.get('a'), None)

    def test_set_existing_key(self):
        cache = LRUCache(limit=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        cache.set('b', 4)

        lst = []
        for elem in cache.cache:
            lst.append(elem)

        self.assertEqual(lst, ['a', 'c', 'b'])

        self.assertEqual(cache.get('a'), 1)
        self.assertEqual(cache.get('b'), 4)
        self.assertEqual(cache.get('c'), 3)
        self.assertEqual(len(cache.cache), 3)

        lst = []
        for elem in cache.cache:
            lst.append(elem)

        self.assertEqual(lst, ['a', 'b', 'c'])

    def test_set_full_cache(self):
        cache = LRUCache(limit=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        cache.set('d', 4)
        self.assertEqual(cache.get('a'), None)
        self.assertEqual(cache.get('b'), 2)
        self.assertEqual(cache.get('c'), 3)
        self.assertEqual(cache.get('d'), 4)
        self.assertEqual(len(cache.cache), 3)

    def test_lru_order(self):
        cache = LRUCache(limit=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        cache.get('a')
        cache.set('d', 4)

        lst = []
        for elem in cache.cache:
            lst.append(elem)

        self.assertEqual(lst, ['c', 'a', 'd'])

        self.assertEqual(cache.get('a'), 1)
        self.assertEqual(cache.get('b'), None)
        self.assertEqual(cache.get('c'), 3)
        self.assertEqual(cache.get('d'), 4)
        self.assertEqual(len(cache.cache), 3)

        lst = []
        for elem in cache.cache:
            lst.append(elem)

        self.assertEqual(lst, ['a', 'c', 'd'])

        cache.get('c')
        cache.set('e', 5)

        lst = []
        for elem in cache.cache:
            lst.append(elem)

        self.assertEqual(lst, ['d', 'c', 'e'])

        self.assertEqual(cache.get('a'), None)
        self.assertEqual(cache.get('c'), 3)
        self.assertEqual(cache.get('d'), 4)
        self.assertEqual(cache.get('e'), 5)
        self.assertEqual(len(cache.cache), 3)

        lst = []
        for elem in cache.cache:
            lst.append(elem)

        self.assertEqual(lst, ['c', 'd', 'e'])

    def test_remove_lru(self):
        cache = LRUCache(limit=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        cache.set('d', 4)
        cache.set('e', 5)
        self.assertEqual(cache.get('a'), None)
        self.assertEqual(cache.get('b'), None)
        self.assertEqual(cache.get('c'), 3)
        self.assertEqual(cache.get('d'), 4)
        self.assertEqual(cache.get('e'), 5)
        self.assertEqual(len(cache.cache), 3)

    def test_cache_effectiveness(self):
        def fib_without_cache(n):
            def fib(i):
                if i < 2:
                    return i

                return fib(i - 1) + fib(i - 2)

            return fib(n)

        def lru_cache(func):
            cache = LRUCache(20)

            def wrapper(*args, **kwargs):
                result = cache.get(args[0])

                if result is not None:
                    return result
                else:
                    result = func(*args, **kwargs)
                    cache.set(args[0], result)
                    return result

            return wrapper

        def fib_with_cache(n):
            @lru_cache
            def fib(i):
                if i < 2:
                    return i

                return fib(i - 1) + fib(i - 2)

            return fib(n)

        beg_time_without_cache = time.time()
        fib1 = fib_without_cache(30)
        end_time_without_cache = time.time() - beg_time_without_cache

        beg_time_with_cache = time.time()
        fib2 = fib_with_cache(30)
        end_time_with_cache = time.time() - beg_time_with_cache

        self.assertEqual(fib1, fib2)
        self.assertLess(end_time_with_cache, end_time_without_cache)


if __name__ == '__main__':
    unittest.main()
