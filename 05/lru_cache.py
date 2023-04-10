class LRUCache:
    def __init__(self, limit=42):
        if not isinstance(limit, int):
            raise TypeError("The cache size must be of type int")

        if limit <= 0:
            raise ValueError("The cache cannot be non-positive size")

        self.limit = limit
        self.cache = {}

    def get(self, key):
        if key not in self.cache:
            return None
        value = self.cache[key]
        self._move_to_end(key)
        return value

    def set(self, key, value):
        if key in self.cache:
            self._move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.limit:
            removed_key = next(iter(self.cache))
            del self.cache[removed_key]

    def _move_to_end(self, key):
        elem = self.cache.pop(key)
        self.cache[key] = elem
