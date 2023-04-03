import unittest
from evaluation_message import SomeModel, predict_message_mood
from unittest import mock


class TestPredictMessageMood(unittest.TestCase):
    def setUp(self):
        self.model = SomeModel()

    def test_predict_message_mood(self):
        with mock.patch.object(SomeModel, 'predict') as func:
            func.return_value = 0.1
            result = predict_message_mood("This is a message 1", self.model)
            self.assertEqual(result, "неуд")
            self.assertEqual([mock.call("This is a message 1")], func.mock_calls)

            func.return_value = 0.5
            result = predict_message_mood("This is a message 2", self.model)
            self.assertEqual(result, "норм")
            self.assertEqual(mock.call("This is a message 2"), func.mock_calls[1])

            func.return_value = 0.9
            result = predict_message_mood("This is a message 3", self.model)
            self.assertEqual(result, "отл")
            self.assertEqual(mock.call("This is a message 3"), func.mock_calls[2])

    def test_predict_message_mood_exact_threshold(self):
        with mock.patch.object(SomeModel, 'predict') as func:
            func.return_value = 0.3
            result = predict_message_mood("This is a message 1", self.model)
            self.assertEqual(result, "норм")
            self.assertEqual([mock.call("This is a message 1")], func.mock_calls)

            func.return_value = 0.8
            result = predict_message_mood("This is a message 2", self.model)
            self.assertEqual(result, "норм")
            self.assertEqual(mock.call("This is a message 2"), func.mock_calls[1])

    def test_predict_message_mood_custom_threshold(self):
        with mock.patch.object(SomeModel, 'predict') as func:
            func.return_value = 0.1
            result = predict_message_mood("This is a message 1", self.model, bad_threshold=0.6, good_threshold=1.7)
            self.assertEqual(result, "неуд")
            self.assertEqual([mock.call("This is a message 1")], func.mock_calls)

            func.return_value = 1.0
            result = predict_message_mood("This is a message 2", self.model, bad_threshold=0.6, good_threshold=1.7)
            self.assertEqual(result, "норм")
            self.assertEqual(mock.call("This is a message 2"), func.mock_calls[1])

            func.return_value = 2.9
            result = predict_message_mood("This is a message 3", self.model, bad_threshold=0.6,
                                          good_threshold=1.7)
            self.assertEqual(result, "отл")
            self.assertEqual(mock.call("This is a message 3"), func.mock_calls[2])

    def test_predict_message_mood_bad_eq_good_threshold(self):
        with mock.patch.object(SomeModel, 'predict') as func:
            func.return_value = 0.5
            result = predict_message_mood("This is a message 1", self.model, bad_threshold=0.5, good_threshold=0.5)
            self.assertEqual(result, "норм")
            self.assertEqual([mock.call("This is a message 1")], func.mock_calls)

            func.return_value = 0.4
            result = predict_message_mood("This is a message 2", self.model, bad_threshold=0.5, good_threshold=0.5)
            self.assertEqual(result, "неуд")
            self.assertEqual(mock.call("This is a message 2"), func.mock_calls[1])

            func.return_value = 0.6
            result = predict_message_mood("This is a message 3", self.model, bad_threshold=0.5, good_threshold=0.5)
            self.assertEqual(result, "отл")
            self.assertEqual(mock.call("This is a message 3"), func.mock_calls[2])

    def test_predict_message_mood_swap_thresholds(self):
        with mock.patch.object(SomeModel, 'predict') as func:
            func.return_value = 0.5
            with self.assertRaises(ValueError) as err:
                predict_message_mood("This is a message", self.model, bad_threshold=0.9, good_threshold=0.2)

            self.assertEqual(str(err.exception), "bad_threshold не может быть больше good_threshold")

    def test_predict_message_mood_predict_exception(self):
        with mock.patch.object(SomeModel, 'predict') as func:
            func.side_effect = Exception
            with self.assertRaises(Exception):
                predict_message_mood("This is a message", self.model)

    def test_predict_message_mood_predict_parameter(self):
        with mock.patch.object(SomeModel, 'predict') as func:
            func.return_value = 0.5
            predict_message_mood("Message", self.model)
            self.assertEqual([mock.call("Message")], func.mock_calls)

    def test_predict_message_mood_predict_return_not_number(self):
        with mock.patch.object(SomeModel, 'predict') as func:
            func.return_value = "jfdshfdjgf"
            with self.assertRaises(TypeError):
                predict_message_mood("This is a message", self.model)

            func.return_value = [1, 2, 4]
            with self.assertRaises(TypeError):
                predict_message_mood("This is a message", self.model)

            func.return_value = (1, 2, 3)
            with self.assertRaises(TypeError):
                predict_message_mood("This is a message", self.model)

            func.return_value = {1, 2, 3}
            with self.assertRaises(TypeError):
                predict_message_mood("This is a message", self.model)

            func.return_value = {1: 2, 2: 3, 3: 4}
            with self.assertRaises(TypeError):
                predict_message_mood("This is a message", self.model)

    def test_predict_message_mood_invalid_parameters(self):
        with self.assertRaises(AttributeError):
            predict_message_mood("This is a message", model=123)

        with mock.patch.object(SomeModel, 'predict') as func:
            func.side_effect = TypeError
            with self.assertRaises(TypeError):
                predict_message_mood(123, SomeModel())

        with self.assertRaises(TypeError):
            predict_message_mood("This is a message", SomeModel(), bad_threshold="bad")

        with self.assertRaises(TypeError):
            predict_message_mood("This is a message", SomeModel(), good_threshold="good")


if __name__ == "__main__":
    unittest.main()
