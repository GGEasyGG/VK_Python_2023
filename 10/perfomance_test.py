import timeit
import json
import cjson
import ujson
from faker import Faker


fake = Faker()

NUM_JSON = 2000
JSON_SIZE = 2000

data = []
for j in range(NUM_JSON):
    json_data = {fake.word(): fake.word() for i in range(JSON_SIZE)}
    data.append(json_data)

json_strings = [json.dumps(obj) for obj in data]
cjson_strings = [cjson.dumps(obj) for obj in data]
ujson_strings = [ujson.dumps(obj) for obj in data]

json_loads_time = timeit.timeit(lambda: [json.loads(json_str) for json_str in json_strings], number=1)

cjson_loads_time = timeit.timeit(lambda: [cjson.loads(json_str) for json_str in cjson_strings], number=1)

ujson_loads_time = timeit.timeit(lambda: [ujson.loads(json_str) for json_str in ujson_strings], number=1)

json_dumps_time = timeit.timeit(lambda: [json.dumps(obj) for obj in data], number=1)

cjson_dumps_time = timeit.timeit(lambda: [cjson.dumps(obj) for obj in data], number=1)

ujson_dumps_time = timeit.timeit(lambda: [ujson.dumps(obj) for obj in data], number=1)

print("json.loads time: {:.3f} seconds".format(json_loads_time))
print("cjson.loads time: {:.3f} seconds".format(cjson_loads_time))
print("ujson.loads time: {:.3f} seconds".format(ujson_loads_time))
print("json.dumps time: {:.3f} seconds".format(json_dumps_time))
print("cjson.dumps time: {:.3f} seconds".format(cjson_dumps_time))
print("ujson.dumps time: {:.3f} seconds".format(ujson_dumps_time))
