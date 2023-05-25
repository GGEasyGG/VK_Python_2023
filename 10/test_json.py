import unittest
import cjson


class CJsonTestCase(unittest.TestCase):
    def test_loads(self):
        json_str = '{"name": "John", "age": 30}'
        expected = {"name": "John", "age": 30}
        result = cjson.loads(json_str)
        self.assertEqual(result, expected)

        json_str = '{      "name"     :      "John"   ,     "age":      30     }'
        expected = {"name": "John", "age": 30}
        result = cjson.loads(json_str)
        self.assertEqual(result, expected)

        json_str = '{"name": "John", "age": "30"}'
        expected = {"name": "John", "age": "30"}
        result = cjson.loads(json_str)
        self.assertEqual(result, expected)

        json_str = '{"name": "John", "age": 30.5}'
        expected = {"name": "John", "age": 30.5}
        result = cjson.loads(json_str)
        self.assertEqual(result, expected)

        invalid_json_str = 123
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected string input")

        invalid_json_str = ''
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Empty JSON string")

        invalid_json_str = '"name": "John", "age": 30}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected object")

        invalid_json_str = '{"name": "John", "age": 30'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected ',' after key and value pair")

        invalid_json_str = '{"name": "John" "age": 30}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected ',' after key and value pair")

        invalid_json_str = '{"name": "John"  . "age": 30}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected ',' after key and value pair")

        invalid_json_str = '{"name": "John "age": 30}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected ',' after key and value pair")

        invalid_json_str = '{"name": "John", "age": 30,'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Invalid JSON string")

        invalid_json_str = '{"name": "John"} "age": 30}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Invalid JSON string")

        invalid_json_str = '{"name"}: "John", "age": 30}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected ':' after object key")

        invalid_json_str = '{name": "John", "age": 30}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected object key")

        invalid_json_str = '{"name": "John", age": 30}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected object key")

        invalid_json_str = '{"name: "John", "age": 30}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected ':' after object key")

        invalid_json_str = '{"name: John, age: 30}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected closing '\"' for object key")

        invalid_json_str = '{"name": "John, age: 30}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected closing '\"' for string value")

        invalid_json_str = '{"name": , "age": 30}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected number value")

        invalid_json_str = '{"name":}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(invalid_json_str)

        self.assertEqual(str(err.exception), "Expected value after ':'")

    def test_dumps(self):
        data = {"name": "John", "age": 30.5}
        expected = '{"name": "John", "age": 30.5}'
        result = cjson.dumps(data)
        self.assertEqual(result, expected)

        data = {"name": "John", "age": 30}
        expected = '{"name": "John", "age": 30}'
        result = cjson.dumps(data)
        self.assertEqual(result, expected)

        data = {"name": "John", "age": "30"}
        expected = '{"name": "John", "age": "30"}'
        result = cjson.dumps(data)
        self.assertEqual(result, expected)

        data = 123
        with self.assertRaises(TypeError) as err:
            cjson.dumps(data)

        self.assertEqual(str(err.exception), "Expected dictionary object")

        data = {123: "John", "age": "30"}
        with self.assertRaises(TypeError) as err:
            cjson.dumps(data)

        self.assertEqual(str(err.exception), "Dictionary keys must be strings")

        data = {"name": [1, 2, 3], "age": "30"}
        with self.assertRaises(TypeError) as err:
            cjson.dumps(data)

        self.assertEqual(str(err.exception), "Dictionary values must be strings or numbers")


if __name__ == '__main__':
    unittest.main()
