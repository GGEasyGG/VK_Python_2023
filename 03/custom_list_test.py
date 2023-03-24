import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def test_custom_list_init_valid_arg(self):
        valid_list = [1, 2, 3, 4]
        custom_list = CustomList(valid_list)
        self.assertEqual(list(custom_list), valid_list)

        valid_tuple = (1, 2, 3, 4)
        custom_list = CustomList(valid_tuple)
        self.assertEqual(list(custom_list), list(valid_tuple))

    def test_custom_list_init_empty_list_or_tuple(self):
        valid_list = []
        custom_list = CustomList(valid_list)
        self.assertEqual(list(custom_list), valid_list)

        valid_tuple = ()
        custom_list = CustomList(valid_tuple)
        self.assertEqual(list(custom_list), list(valid_tuple))

    def test_custom_list_init_invalid_arg(self):
        with self.assertRaises(TypeError) as err:
            CustomList(20)
        self.assertEqual(str(err.exception), 'CustomList can be created only based on a list or a tuple')

        with self.assertRaises(TypeError) as err:
            CustomList(65.89)
        self.assertEqual(str(err.exception), 'CustomList can be created only based on a list or a tuple')

        with self.assertRaises(TypeError) as err:
            CustomList('invalid')
        self.assertEqual(str(err.exception), 'CustomList can be created only based on a list or a tuple')

        with self.assertRaises(TypeError) as err:
            CustomList({1: 2, 2: 3})
        self.assertEqual(str(err.exception), 'CustomList can be created only based on a list or a tuple')

        with self.assertRaises(TypeError) as err:
            CustomList({1, 2, 3})
        self.assertEqual(str(err.exception), 'CustomList can be created only based on a list or a tuple')

        with self.assertRaises(TypeError) as err:
            CustomList(True)
        self.assertEqual(str(err.exception), 'CustomList can be created only based on a list or a tuple')

    def test_custom_list_init_invalid_type(self):
        with self.assertRaises(TypeError) as err:
            CustomList([1, [2, 3], 'invalid', (4, 5, 6), {1: 1, 2: 2}, {1, 2}, 6.7, False])
        self.assertEqual(str(err.exception), 'CustomList elements must be of type int or float')

        with self.assertRaises(TypeError) as err:
            CustomList((1, [2, 3], 'invalid', (4, 5, 6), {1: 1, 2: 2}, {1, 2}, 6.7, False))
        self.assertEqual(str(err.exception), 'CustomList elements must be of type int or float')

    def test_custom_list_add_custom_list(self):
        custom_list_1 = CustomList([1, 2, 3, 4])
        custom_list_2 = CustomList([5, 6, 7, 8])
        expected_result = CustomList([6, 8, 10, 12])
        self.assertEqual(custom_list_1 + custom_list_2, expected_result)

        custom_list_1 = CustomList([1.1, 2.2, 3.3, 4.4])
        custom_list_2 = CustomList([5.1, 6.2, 7.3, 8.4])
        expected_result = CustomList([6.2, 8.4, 10.6, 12.8])
        self.assertEqual(custom_list_1 + custom_list_2, expected_result)

        custom_list_1 = CustomList([1.1, 2.2, 3.3, 4.4])
        custom_list_2 = CustomList([5, 6, 7, 8])
        expected_result = CustomList([6.1, 8.2, 10.3, 12.4])
        self.assertEqual(custom_list_1 + custom_list_2, expected_result)

        custom_list_1 = CustomList([1.1, 2, 3.3, 4])
        custom_list_2 = CustomList([5, 6.2, 7, 8.4])
        expected_result = CustomList([6.1, 8.2, 10.3, 12.4])
        self.assertEqual(custom_list_1 + custom_list_2, expected_result)

    def test_custom_list_add_custom_list_with_different_length(self):
        custom_list_1 = CustomList([1, 2])
        custom_list_2 = CustomList([5, 6, 7, 8])
        expected_result = CustomList([6, 8, 7, 8])
        self.assertEqual(custom_list_1 + custom_list_2, expected_result)

        custom_list_1 = CustomList([1, 2, 3])
        custom_list_2 = CustomList([5, 6, 7, 8])
        expected_result = CustomList([6, 8, 10, 8])
        self.assertEqual(custom_list_1 + custom_list_2, expected_result)

        custom_list_1 = CustomList([1])
        custom_list_2 = CustomList([5, 6, 7, 8])
        expected_result = CustomList([6, 6, 7, 8])
        self.assertEqual(custom_list_1 + custom_list_2, expected_result)

        custom_list_1 = CustomList([])
        custom_list_2 = CustomList([5, 6, 7, 8])
        expected_result = CustomList([5, 6, 7, 8])
        self.assertEqual(custom_list_1 + custom_list_2, expected_result)

    def test_custom_list_add_default_list(self):
        custom_list = CustomList([1, 2, 3, 4])
        default_list = [5, 6, 7, 8]
        expected_result = CustomList([6, 8, 10, 12])
        self.assertEqual(custom_list + default_list, expected_result)
        self.assertEqual(default_list + custom_list, expected_result)

        custom_list = CustomList([1.1, 2.2, 3.3, 4.4])
        default_list = [5, 6, 7, 8]
        expected_result = CustomList([6.1, 8.2, 10.3, 12.4])
        self.assertEqual(custom_list + default_list, expected_result)
        self.assertEqual(default_list + custom_list, expected_result)

        custom_list = CustomList([1, 2, 3, 4])
        default_list = [5.1, 6.2, 7.3, 8.4]
        expected_result = CustomList([6.1, 8.2, 10.3, 12.4])
        self.assertEqual(custom_list + default_list, expected_result)
        self.assertEqual(default_list + custom_list, expected_result)

        custom_list = CustomList([1.1, 2.2, 3.3, 4.4])
        default_list = [5.1, 6.2, 7.3, 8.4]
        expected_result = CustomList([6.2, 8.4, 10.6, 12.8])
        self.assertEqual(custom_list + default_list, expected_result)
        self.assertEqual(default_list + custom_list, expected_result)

        custom_list = CustomList([1, 2.2, 3, 4.4])
        default_list = [5.1, 6, 7.3, 8]
        expected_result = CustomList([6.1, 8.2, 10.3, 12.4])
        self.assertEqual(custom_list + default_list, expected_result)
        self.assertEqual(default_list + custom_list, expected_result)

    def test_custom_list_add_default_list_with_different_length(self):
        custom_list = CustomList([1, 2])
        default_list = CustomList([5, 6, 7, 8])
        expected_result = CustomList([6, 8, 7, 8])
        self.assertEqual(custom_list + default_list, expected_result)

        custom_list = CustomList([1, 2, 3, 4])
        default_list = CustomList([5, 6])
        expected_result = CustomList([6, 8, 3, 4])
        self.assertEqual(custom_list + default_list, expected_result)

        custom_list = CustomList([1, 2, 3])
        default_list = CustomList([5, 6, 7, 8])
        expected_result = CustomList([6, 8, 10, 8])
        self.assertEqual(custom_list + default_list, expected_result)

        custom_list = CustomList([1, 2, 3, 4])
        default_list = CustomList([5, 6, 7])
        expected_result = CustomList([6, 8, 10, 4])
        self.assertEqual(custom_list + default_list, expected_result)

        custom_list = CustomList([1])
        default_list = CustomList([5, 6, 7, 8])
        expected_result = CustomList([6, 6, 7, 8])
        self.assertEqual(custom_list + default_list, expected_result)

        custom_list = CustomList([1, 2, 3, 4])
        default_list = CustomList([5])
        expected_result = CustomList([6, 2, 3, 4])
        self.assertEqual(custom_list + default_list, expected_result)

        custom_list = CustomList([])
        default_list = CustomList([5, 6, 7, 8])
        expected_result = CustomList([5, 6, 7, 8])
        self.assertEqual(custom_list + default_list, expected_result)

        custom_list = CustomList([1, 2, 3, 4])
        default_list = CustomList([])
        expected_result = CustomList([1, 2, 3, 4])
        self.assertEqual(custom_list + default_list, expected_result)

    def test_custom_list_add_invalid_type(self):
        custom_list = CustomList([1, 2, 3, 4])
        invalid_arg = 'invalid'
        with self.assertRaises(TypeError) as err:
            custom_list + invalid_arg
        self.assertEqual(str(err.exception), 'Only the CustomList and default list can be added to the CustomList')

        with self.assertRaises(TypeError) as err:
            invalid_arg + custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList and default list can be added to the CustomList')

        custom_list = CustomList([1, 2, 3, 4])
        invalid_arg = [1, [2, 3], 'invalid', 4]
        with self.assertRaises(TypeError) as err:
            custom_list + invalid_arg
        self.assertEqual(str(err.exception),
                         'Only default list with elements of int or float type can be added to the CustomList')

        with self.assertRaises(TypeError) as err:
            invalid_arg + custom_list
        self.assertEqual(str(err.exception),
                         'Only default list with elements of int or float type can be added to the CustomList')

    def test_custom_list_subtract_custom_list(self):
        custom_list_1 = CustomList([1, 2, 3, 4])
        custom_list_2 = CustomList([5, 6, 7, 8])
        expected_result = CustomList([-4, -4, -4, -4])
        self.assertEqual(custom_list_1 - custom_list_2, expected_result)

        custom_list_1 = CustomList([1.1, 2.2, 3.3, 4.4])
        custom_list_2 = CustomList([5.1, 6.2, 7.3, 8.4])
        expected_result = CustomList([-4.0, -4.0, -4.0, -4.0])
        self.assertEqual(custom_list_1 - custom_list_2, expected_result)

        custom_list_1 = CustomList([1.1, 2.2, 3.3, 4.4])
        custom_list_2 = CustomList([5, 6, 7, 8])
        expected_result = CustomList([-3.9, -3.8, -3.7, -3.6])
        self.assertEqual(custom_list_1 - custom_list_2, expected_result)

        custom_list_1 = CustomList([1.1, 2, 3.3, 4])
        custom_list_2 = CustomList([5, 6.2, 7, 8.4])
        expected_result = CustomList([-3.9, -4.2, -3.7, -4.4])
        self.assertEqual(custom_list_1 - custom_list_2, expected_result)

    def test_custom_list_sub_custom_list_with_different_length(self):
        custom_list_1 = CustomList([1, 2])
        custom_list_2 = CustomList([5, 6, 7, 8])
        expected_result = CustomList([-4, -4, -7, -8])
        self.assertEqual(custom_list_1 - custom_list_2, expected_result)

        custom_list_1 = CustomList([1, 2, 3])
        custom_list_2 = CustomList([5, 6, 7, 8])
        expected_result = CustomList([-4, -4, -4, -8])
        self.assertEqual(custom_list_1 - custom_list_2, expected_result)

        custom_list_1 = CustomList([1])
        custom_list_2 = CustomList([5, 6, 7, 8])
        expected_result = CustomList([-4, -6, -7, -8])
        self.assertEqual(custom_list_1 - custom_list_2, expected_result)

        custom_list_1 = CustomList([])
        custom_list_2 = CustomList([5, 6, 7, 8])
        expected_result = CustomList([-5, -6, -7, -8])
        self.assertEqual(custom_list_1 - custom_list_2, expected_result)

    def test_custom_list_subtract_default_list(self):
        custom_list = CustomList([1, 2, 3, 4])
        default_list = [5, 6, 7, 8]
        expected_result1 = CustomList([-4, -4, -4, -4])
        expected_result2 = CustomList([4, 4, 4, 4])
        self.assertEqual(custom_list - default_list, expected_result1)
        self.assertEqual(default_list - custom_list, expected_result2)

        custom_list = CustomList([1.1, 2.2, 3.3, 4.4])
        default_list = [5, 6, 7, 8]
        expected_result1 = CustomList([-3.9, -3.8, -3.7, -3.6])
        expected_result2 = CustomList([3.9, 3.8, 3.7, 3.6])
        self.assertEqual(custom_list - default_list, expected_result1)
        self.assertEqual(default_list - custom_list, expected_result2)

        custom_list = CustomList([1, 2, 3, 4])
        default_list = [5.1, 6.2, 7.3, 8.4]
        expected_result1 = CustomList([-4.1, -4.2, -4.3, -4.4])
        expected_result2 = CustomList([4.1, 4.2, 4.3, 4.4])
        self.assertEqual(custom_list - default_list, expected_result1)
        self.assertEqual(default_list - custom_list, expected_result2)

        custom_list = CustomList([1.1, 2.2, 3.3, 4.4])
        default_list = [5.1, 6.2, 7.3, 8.4]
        expected_result1 = CustomList([-4.0, -4.0, -4.0, -4.0])
        expected_result2 = CustomList([4.0, 4.0, 4.0, 4.0])
        self.assertEqual(custom_list - default_list, expected_result1)
        self.assertEqual(default_list - custom_list, expected_result2)

        custom_list = CustomList([1, 2.2, 3, 4.4])
        default_list = [5.1, 6, 7.3, 8]
        expected_result1 = CustomList([-4.1, -3.8, -4.3, -3.6])
        expected_result2 = CustomList([4.1, 3.8, 4.3, 3.6])
        self.assertEqual(custom_list - default_list, expected_result1)
        self.assertEqual(default_list - custom_list, expected_result2)

    def test_custom_list_sub_default_list_with_different_length(self):
        custom_list = CustomList([1, 2])
        default_list = CustomList([5, 6, 7, 8])
        expected_result1 = CustomList([-4, -4, -7, -8])
        expected_result2 = CustomList([4, 4, 7, 8])
        self.assertEqual(custom_list - default_list, expected_result1)
        self.assertEqual(default_list - custom_list, expected_result2)

        custom_list = CustomList([1, 2, 3, 4])
        default_list = CustomList([5, 6])
        expected_result1 = CustomList([-4, -4, 3, 4])
        expected_result2 = CustomList([4, 4, -3, -4])
        self.assertEqual(custom_list - default_list, expected_result1)
        self.assertEqual(default_list - custom_list, expected_result2)

        custom_list = CustomList([1, 2, 3])
        default_list = CustomList([5, 6, 7, 8])
        expected_result1 = CustomList([-4, -4, -4, -8])
        expected_result2 = CustomList([4, 4, 4, 8])
        self.assertEqual(custom_list - default_list, expected_result1)
        self.assertEqual(default_list - custom_list, expected_result2)

        custom_list = CustomList([1, 2, 3, 4])
        default_list = CustomList([5, 6, 7])
        expected_result1 = CustomList([-4, -4, -4, 4])
        expected_result2 = CustomList([4, 4, 4, -4])
        self.assertEqual(custom_list - default_list, expected_result1)
        self.assertEqual(default_list - custom_list, expected_result2)

        custom_list = CustomList([1])
        default_list = CustomList([5, 6, 7, 8])
        expected_result1 = CustomList([-4, -6, -7, -8])
        expected_result2 = CustomList([4, 6, 7, 8])
        self.assertEqual(custom_list - default_list, expected_result1)
        self.assertEqual(default_list - custom_list, expected_result2)

        custom_list = CustomList([1, 2, 3, 4])
        default_list = CustomList([5])
        expected_result1 = CustomList([-4, 2, 3, 4])
        expected_result2 = CustomList([4, -2, -3, -4])
        self.assertEqual(custom_list - default_list, expected_result1)
        self.assertEqual(default_list - custom_list, expected_result2)

        custom_list = CustomList([])
        default_list = CustomList([5, 6, 7, 8])
        expected_result1 = CustomList([-5, -6, -7, -8])
        expected_result2 = CustomList([5, 6, 7, 8])
        self.assertEqual(custom_list - default_list, expected_result1)
        self.assertEqual(default_list - custom_list, expected_result2)

        custom_list = CustomList([1, 2, 3, 4])
        default_list = CustomList([])
        expected_result1 = CustomList([1, 2, 3, 4])
        expected_result2 = CustomList([-1, -2, -3, -4])
        self.assertEqual(custom_list - default_list, expected_result1)
        self.assertEqual(default_list - custom_list, expected_result2)

    def test_custom_list_subtract_invalid_type(self):
        custom_list = CustomList([1, 2, 3, 4])
        invalid_arg = 'invalid'
        with self.assertRaises(TypeError) as err:
            custom_list - invalid_arg
        self.assertEqual(str(err.exception),
                         'Only the CustomList and default list can be subtracted with the CustomList')

        with self.assertRaises(TypeError) as err:
            invalid_arg - custom_list
        self.assertEqual(str(err.exception),
                         'Only the CustomList and default list can be subtracted with the CustomList')

        custom_list = CustomList([1, 2, 3, 4])
        invalid_arg = [1, [2, 3], 'invalid', 4]
        with self.assertRaises(TypeError) as err:
            custom_list - invalid_arg
        self.assertEqual(str(err.exception),
                         'Only default list with elements of int or float type can be subtracted with the CustomList')

        with self.assertRaises(TypeError) as err:
            invalid_arg - custom_list
        self.assertEqual(str(err.exception),
                         'Only default list with elements of int or float type can be subtracted with the CustomList')

    def test_eq(self):
        self.assertTrue(CustomList([1, 2, 3]) == CustomList([1, 2, 3]))
        self.assertTrue(CustomList([]) == CustomList([]))
        self.assertTrue(CustomList([1, -1]) == CustomList([0, 0, 0]))
        self.assertTrue(CustomList([1, 2, 3, 4]) == CustomList([2, 2, 3, 3]))
        self.assertTrue(CustomList([]) == CustomList([0, 0, 0]))

        self.assertFalse(CustomList([1, 2, 3]) == CustomList([1, 2, 4]))
        self.assertFalse(CustomList([1, 2, 3, 4]) == CustomList([1, 2, 4]))
        self.assertFalse(CustomList([]) == CustomList([1]))

    def test_ne(self):
        self.assertTrue(CustomList([1, 2, 3]) != CustomList([1, 2, 4]))
        self.assertTrue(CustomList([1, 2, 3, 4]) != CustomList([1, 2, 4]))
        self.assertTrue(CustomList([]) != CustomList([1]))

        self.assertFalse(CustomList([1, 2, 3]) != CustomList([1, 2, 3]))
        self.assertFalse(CustomList([]) != CustomList([]))
        self.assertFalse(CustomList([1, -1]) != CustomList([0, 0, 0]))
        self.assertFalse(CustomList([1, 2, 3, 4]) != CustomList([2, 2, 3, 3]))
        self.assertFalse(CustomList([]) != CustomList([0, 0, 0]))

    def test_lt(self):
        self.assertTrue(CustomList([1, 2, 3]) < CustomList([1, 2, 4]))
        self.assertTrue(CustomList([1, 2, 3]) < CustomList([1, 2, 3, 4]))
        self.assertTrue(CustomList([]) < CustomList([1]))
        self.assertTrue(CustomList([-1, -2, -3]) < CustomList([0, -2, -3]))

        self.assertFalse(CustomList([1, 2, 4]) < CustomList([1, 2, 3]))
        self.assertFalse(CustomList([1, 2, 3, 4]) < CustomList([1, 2, 3]))
        self.assertFalse(CustomList([1]) < CustomList([]))
        self.assertFalse(CustomList([0, -2, -3]) < CustomList([-1, -2, -3]))

    def test_le(self):
        self.assertTrue(CustomList([1, 2, 3]) <= CustomList([1, 2, 4]))
        self.assertTrue(CustomList([1, 2, 3]) <= CustomList([1, 2, 3, 4]))
        self.assertTrue(CustomList([]) <= CustomList([1]))
        self.assertTrue(CustomList([-1, -2, -3]) <= CustomList([0, -2, -3]))
        self.assertTrue(CustomList([-1, -2, -3]) <= CustomList([-1, -2, -3]))
        self.assertTrue(CustomList([1, 2, 3]) <= CustomList([1, 2, 3]))
        self.assertTrue(CustomList([]) <= CustomList([-1, 0, 1]))

        self.assertFalse(CustomList([1, 2, 4]) <= CustomList([1, 2, 3]))
        self.assertFalse(CustomList([1, 2, 3, 4]) <= CustomList([1, 2, 3]))
        self.assertFalse(CustomList([1]) <= CustomList([0]))
        self.assertFalse(CustomList([0, -2, -3]) <= CustomList([-1, -2, -3]))

    def test_gt(self):
        self.assertFalse(CustomList([1, 2, 3]) > CustomList([1, 2, 4]))
        self.assertFalse(CustomList([1, 2, 3]) > CustomList([1, 2, 3, 4]))
        self.assertFalse(CustomList([]) > CustomList([1]))
        self.assertFalse(CustomList([-1, -2, -3]) > CustomList([0, -2, -3]))

        self.assertTrue(CustomList([1, 2, 4]) > CustomList([1, 2, 3]))
        self.assertTrue(CustomList([1, 2, 3, 4]) > CustomList([1, 2, 3]))
        self.assertTrue(CustomList([1]) > CustomList([]))
        self.assertTrue(CustomList([0, -2, -3]) > CustomList([-1, -2, -3]))

    def test_ge(self):
        self.assertFalse(CustomList([1, 2, 3]) >= CustomList([1, 2, 4]))
        self.assertFalse(CustomList([1, 2, 3]) >= CustomList([1, 2, 3, 4]))
        self.assertFalse(CustomList([]) >= CustomList([1]))
        self.assertFalse(CustomList([-1, -2, -3]) >= CustomList([0, -2, -3]))
        self.assertTrue(CustomList([-1, -2, -3]) >= CustomList([-1, -2, -3]))
        self.assertTrue(CustomList([1, 2, 3]) >= CustomList([1, 2, 3]))
        self.assertTrue(CustomList([]) >= CustomList([-1, 0, 1]))

        self.assertTrue(CustomList([1, 2, 4]) >= CustomList([1, 2, 3]))
        self.assertTrue(CustomList([1, 2, 3, 4]) >= CustomList([1, 2, 3]))
        self.assertTrue(CustomList([1]) >= CustomList([]))
        self.assertTrue(CustomList([0, -2, -3]) >= CustomList([-1, -2, -3]))

    def test_eq_invalid_type(self):
        custom_list = CustomList([1, 2, 3, 4])

        invalid_type = 20
        with self.assertRaises(TypeError) as err:
            custom_list == invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type == custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = 65.89
        with self.assertRaises(TypeError) as err:
            custom_list == invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type == custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = 'invalid'
        with self.assertRaises(TypeError) as err:
            custom_list == invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type == custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = {1: 2, 2: 3}
        with self.assertRaises(TypeError) as err:
            custom_list == invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type == custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = {1, 2, 3}
        with self.assertRaises(TypeError) as err:
            custom_list == invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type == custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = True
        with self.assertRaises(TypeError) as err:
            custom_list == invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type == custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

    def test_ne_invalid_type(self):
        custom_list = CustomList([1, 2, 3, 4])

        invalid_type = 20
        with self.assertRaises(TypeError) as err:
            custom_list != invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type != custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = 65.89
        with self.assertRaises(TypeError) as err:
            custom_list != invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type != custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = 'invalid'
        with self.assertRaises(TypeError) as err:
            custom_list != invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type != custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = {1: 2, 2: 3}
        with self.assertRaises(TypeError) as err:
            custom_list != invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type != custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = {1, 2, 3}
        with self.assertRaises(TypeError) as err:
            custom_list != invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type != custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = True
        with self.assertRaises(TypeError) as err:
            custom_list != invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type != custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

    def test_lt_invalid_type(self):
        custom_list = CustomList([1, 2, 3, 4])

        invalid_type = 20
        with self.assertRaises(TypeError) as err:
            custom_list < invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type < custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = 65.89
        with self.assertRaises(TypeError) as err:
            custom_list < invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type < custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = 'invalid'
        with self.assertRaises(TypeError) as err:
            custom_list < invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type < custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = {1: 2, 2: 3}
        with self.assertRaises(TypeError) as err:
            custom_list < invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type < custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = {1, 2, 3}
        with self.assertRaises(TypeError) as err:
            custom_list < invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type < custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = True
        with self.assertRaises(TypeError) as err:
            custom_list < invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type < custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

    def test_le_invalid_type(self):
        custom_list = CustomList([1, 2, 3, 4])

        invalid_type = 20
        with self.assertRaises(TypeError) as err:
            custom_list <= invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type <= custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = 65.89
        with self.assertRaises(TypeError) as err:
            custom_list <= invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type <= custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = 'invalid'
        with self.assertRaises(TypeError) as err:
            custom_list <= invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type <= custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = {1: 2, 2: 3}
        with self.assertRaises(TypeError) as err:
            custom_list <= invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type <= custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = {1, 2, 3}
        with self.assertRaises(TypeError) as err:
            custom_list <= invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type <= custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = True
        with self.assertRaises(TypeError) as err:
            custom_list <= invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type <= custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

    def test_gt_invalid_type(self):
        custom_list = CustomList([1, 2, 3, 4])

        invalid_type = 20
        with self.assertRaises(TypeError) as err:
            custom_list > invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type > custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = 65.89
        with self.assertRaises(TypeError) as err:
            custom_list > invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type > custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = 'invalid'
        with self.assertRaises(TypeError) as err:
            custom_list > invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type > custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = {1: 2, 2: 3}
        with self.assertRaises(TypeError) as err:
            custom_list > invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type > custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = {1, 2, 3}
        with self.assertRaises(TypeError) as err:
            custom_list > invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type > custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = True
        with self.assertRaises(TypeError) as err:
            custom_list > invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type > custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

    def test_ge_invalid_type(self):
        custom_list = CustomList([1, 2, 3, 4])

        invalid_type = 20
        with self.assertRaises(TypeError) as err:
            custom_list >= invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type >= custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = 65.89
        with self.assertRaises(TypeError) as err:
            custom_list >= invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type >= custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = 'invalid'
        with self.assertRaises(TypeError) as err:
            custom_list >= invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type >= custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = {1: 2, 2: 3}
        with self.assertRaises(TypeError) as err:
            custom_list >= invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type >= custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = {1, 2, 3}
        with self.assertRaises(TypeError) as err:
            custom_list >= invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type >= custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

        invalid_type = True
        with self.assertRaises(TypeError) as err:
            custom_list >= invalid_type
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')
        with self.assertRaises(TypeError) as err:
            invalid_type >= custom_list
        self.assertEqual(str(err.exception), 'Only the CustomList can be compared')

    def test_str_method(self):
        self.assertEqual(str(CustomList([1, 2, 3])), '[1, 2, 3], 6')
        self.assertEqual(str(CustomList([0, 0, 0, 0])), '[0, 0, 0, 0], 0')
        self.assertEqual(str(CustomList([-1, 0, 1])), '[-1, 0, 1], 0')
        self.assertEqual(str(CustomList([3.14, 2.71])), '[3.14, 2.71], 5.85')
        self.assertEqual(str(CustomList([])), '[], 0')
