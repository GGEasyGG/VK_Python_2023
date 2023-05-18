import logging
import sys


class LRUCache:
    def __init__(self, limit=42):
        self.filter_enabled = "-f" in sys.argv
        self.logger = self._setup_logger()

        if not isinstance(limit, int):
            raise TypeError("The cache size must be of type int")

        if limit <= 0:
            raise ValueError("The cache cannot be a non-positive size")

        self.limit = limit
        self.cache = {}

    def get(self, key):
        if key not in self.cache:
            self.logger.info("Key '%s' not found in cache", key)
            return None
        value = self.cache[key]
        self._move_to_end(key)
        self.logger.info("Key '%s' retrieved from cache: %s", key, value)
        return value

    def set(self, key, value):
        if key in self.cache:
            self.logger.info("Key '%s' already exists in cache", key)
            self._move_to_end(key)
        else:
            self.logger.info("Key '%s' added to cache", key)
        self.cache[key] = value
        if len(self.cache) > self.limit:
            removed_key = next(iter(self.cache))
            del self.cache[removed_key]
            self.logger.info("Capacity limit reached. Key '%s' evicted from cache", removed_key)

    def _move_to_end(self, key):
        elem = self.cache.pop(key)
        self.cache[key] = elem
        self.logger.debug("Key '%s' moved to end", key)

    def _setup_logger(self):
        logger = logging.getLogger("LRUCache")
        logger.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler = logging.FileHandler("cache.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)

        if self.filter_enabled:
            file_handler.addFilter(self._apply_filter)

        logger.addHandler(file_handler)

        if "-s" in sys.argv:
            stdout_formatter = logging.Formatter("%(levelname)s: %(message)s")
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logging.DEBUG)
            stdout_handler.setFormatter(stdout_formatter)

            if self.filter_enabled:
                stdout_handler.addFilter(self._apply_filter)

            logger.addHandler(stdout_handler)

        return logger

    def _apply_filter(self, record):
        if self.filter_enabled:
            message = record.getMessage()
            words = message.split()
            if len(words) % 2 == 0:
                return False
        return True


if __name__ == "__main__":
    cache = LRUCache(limit=3)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    cache.set("key1", "value6")
    cache.get("key1")
    cache.get("key2")
    cache.get("key4")
    cache.set("key4", "value4")
    cache.set("key5", "value5")
