import weakref
import time
import cProfile
import functools


class NormalClass:
    def __init__(self, s, n):
        self.s = s
        self.n = n


class SlotsClass:
    slots = ['s', 'n']

    def __init__(self, s, n):
        self.s = s
        self.n = n


class WeakrefClass:
    def __init__(self, s, n):
        self.s = weakref.ref(s)
        self.n = weakref.ref(n)


class TestClass(dict):
    pass


start = time.time()
normal_instances = [NormalClass('abc', i) for i in range(1000000)]
end = time.time()
print(f"Time to create 1 million NormalClass instances: {end - start:.3f} seconds")

start = time.time()
slots_instances = [SlotsClass('abc', i) for i in range(1000000)]
end = time.time()
print(f"Time to create 1 million SlotsClass instances: {end - start:.3f} seconds")

start = time.time()
weakref_instances = [WeakrefClass(TestClass(), TestClass()) for i in range(1000000)]
end = time.time()
print(f"Time to create 1 million WeakrefClass instances: {end - start:.3f} seconds")
start = time.time()
for instance in normal_instances:
    instance.s
    instance.n += 1
end = time.time()
print(f"Time to read and change attributes of NormalClass instances: {end - start:.3f} seconds")

start = time.time()
for instance in slots_instances:
    instance.s
    instance.n += 1
end = time.time()
print(f"Time to read and change attributes of SlotsClass instances: {end - start:.3f} seconds")

start = time.time()
for instance in weakref_instances:
    instance.s()
    instance.n()
end = time.time()
print(f"Time to read and change attributes of WeakrefClass instances: {end - start:.3f} seconds")


def test():
    normal_instances = [NormalClass('abc', i) for i in range(1000000)]

    for instance in normal_instances:
        instance.s
        instance.n += 1

    slots_instances = [SlotsClass('abc', i) for i in range(1000000)]

    for instance in slots_instances:
        instance.s
        instance.n += 1

    weakref_instances = [WeakrefClass(TestClass(), TestClass()) for i in range(1000000)]

    for instance in weakref_instances:
        instance.s()
        instance.n()


cProfile.run('test()', sort='cumulative')


def profile_deco(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        wrapper.profiler = profiler
        return result
    return wrapper


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


add(1, 2)
add(4, 5)
sub(4, 5)

add.profiler.print_stats()
sub.profiler.print_stats()
