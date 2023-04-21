import unittest
from custom_meta import CustomMeta


class TestCustomMeta(unittest.TestCase):
    def setUp(self):
        class TestClass(metaclass=CustomMeta):
            my_attr = 42

            def __init__(self):
                self.a = '123'
                self.b = 19.7

            def abc(self):
                return '123'

            def __str__(self):
                return 'TestClass'

        class Derived(TestClass):
            x = 12
            __qwe__ = 67

        self.child_cls = Derived
        self.cls = TestClass
        self.obj = TestClass()
        self.child = Derived()

    def test_class_attribute(self):
        self.assertTrue(hasattr(self.cls, "custom_my_attr"))
        self.assertFalse(hasattr(self.cls, "my_attr"))
        self.assertEqual(self.cls.custom_my_attr, 42)

        self.assertTrue(hasattr(self.cls, "custom_abc"))
        self.assertFalse(hasattr(self.cls, "abc"))

        self.assertTrue(hasattr(self.cls, "__str__"))
        self.assertFalse(hasattr(self.cls, "custom___str__"))

    def test_child_class_attribute(self):
        self.assertTrue(hasattr(self.child_cls, "custom_x"))
        self.assertFalse(hasattr(self.child_cls, "x"))
        self.assertEqual(self.child_cls.custom_x, 12)

        self.assertTrue(hasattr(self.child_cls, "__qwe__"))
        self.assertFalse(hasattr(self.child_cls, "custom___qwe__"))
        self.assertEqual(self.child_cls.__qwe__, 67)

        self.assertTrue(hasattr(self.child_cls, "custom_my_attr"))
        self.assertFalse(hasattr(self.child_cls, "my_attr"))
        self.assertEqual(self.child_cls.custom_my_attr, 42)

        self.assertTrue(hasattr(self.child_cls, "custom_abc"))
        self.assertFalse(hasattr(self.child_cls, "abc"))

        self.assertTrue(hasattr(self.child_cls, "__str__"))
        self.assertFalse(hasattr(self.child_cls, "custom___str__"))

    def test_custom_attribute(self):
        self.assertTrue(hasattr(self.obj, "custom_my_attr"))
        self.assertFalse(hasattr(self.obj, "my_attr"))
        self.assertEqual(self.obj.custom_my_attr, 42)

        self.assertTrue(hasattr(self.obj, "custom_a"))
        self.assertFalse(hasattr(self.obj, "a"))
        self.assertEqual(self.obj.custom_a, '123')

        self.assertTrue(hasattr(self.obj, "custom_b"))
        self.assertFalse(hasattr(self.obj, "b"))
        self.assertEqual(self.obj.custom_b, 19.7)

        self.assertTrue(hasattr(self.obj, "custom_abc"))
        self.assertFalse(hasattr(self.obj, "abc"))
        self.assertEqual(self.obj.custom_abc(), '123')

        self.assertTrue(hasattr(self.obj, "__str__"))
        self.assertFalse(hasattr(self.obj, "custom___str__"))
        self.assertEqual(str(self.obj), "TestClass")

    def test_added_builtin_attribute(self):
        setattr(self.obj, "__abc__", 10)
        self.assertTrue(hasattr(self.obj, '__abc__'))
        self.assertFalse(hasattr(self.obj, 'custom___abc__'))
        self.assertEqual(self.obj.__abc__, 10)

    def test_added_attribute(self):
        self.obj.d = 16.16
        self.assertTrue(hasattr(self.obj, 'custom_d'))
        self.assertFalse(hasattr(self.obj, 'd'))
        self.assertEqual(self.obj.custom_d, 16.16)

    def test_overriding_custom_attribute(self):
        self.obj.custom_my_attr = 10
        self.assertTrue(hasattr(self.obj, "custom_my_attr"))
        self.assertFalse(hasattr(self.obj, "custom_custom_my_attr"))
        self.assertEqual(self.obj.custom_my_attr, 10)

        self.obj.custom_a = 20
        self.assertTrue(hasattr(self.obj, "custom_a"))
        self.assertFalse(hasattr(self.obj, "custom_custom_a"))
        self.assertEqual(self.obj.custom_a, 20)

        self.obj.custom_b = 30
        self.assertTrue(hasattr(self.obj, "custom_b"))
        self.assertFalse(hasattr(self.obj, "custom_custom_b"))
        self.assertEqual(self.obj.custom_b, 30)

    def test_accessing_custom_attribute_through_base_class(self):
        self.assertTrue(hasattr(self.child, "custom_my_attr"))
        self.assertFalse(hasattr(self.child, "my_attr"))
        self.assertEqual(self.child.custom_my_attr, 42)

        self.assertTrue(hasattr(self.child, "custom_a"))
        self.assertFalse(hasattr(self.child, "a"))
        self.assertEqual(self.child.custom_a, '123')

        self.assertTrue(hasattr(self.child, "custom_b"))
        self.assertFalse(hasattr(self.child, "b"))
        self.assertEqual(self.child.custom_b, 19.7)

        self.assertTrue(hasattr(self.child, "custom_abc"))
        self.assertFalse(hasattr(self.child, "abc"))
        self.assertEqual(self.child.custom_abc(), '123')

        self.assertTrue(hasattr(self.child, "__str__"))
        self.assertFalse(hasattr(self.child, "custom___str__"))
        self.assertEqual(str(self.child), "TestClass")

    def test_custom_attribute_from_child_class(self):
        self.assertEqual(self.child.custom_x, 12)
        self.assertTrue(hasattr(self.child, "custom_x"))
        self.assertFalse(hasattr(self.child, "x"))

        self.assertEqual(self.child.__qwe__, 67)
        self.assertTrue(hasattr(self.child, "__qwe__"))
        self.assertFalse(hasattr(self.child, "custom___qwe__"))

    def test_added_attribute_to_child_class(self):
        self.child.y = 'qwerty'
        self.assertEqual(self.child.custom_y, 'qwerty')
        self.assertTrue(hasattr(self.child, "custom_y"))
        self.assertFalse(hasattr(self.child, "y"))

    def test_added_builtin_attribute_to_child_class(self):
        self.child.__z__ = None
        self.assertIsNone(self.child.__z__)
        self.assertTrue(hasattr(self.child, "__z__"))
        self.assertFalse(hasattr(self.child, "custom___z__"))

    def test_overriding_custom_attribute_in_child_class(self):
        self.child.custom_x = 10
        self.assertTrue(hasattr(self.child, "custom_x"))
        self.assertFalse(hasattr(self.child, "custom_custom_x"))
        self.assertEqual(self.child.custom_x, 10)

    def test_overriding_builtin_attribute_in_child_class(self):
        self.assertTrue(hasattr(self.child, "__qwe__"))
        self.assertFalse(hasattr(self.child, "custom___qwe__"))
        self.child.__qwe__ = 10
        self.assertTrue(hasattr(self.child, "__qwe__"))
        self.assertFalse(hasattr(self.child, "custom___qwe__"))
        self.assertEqual(self.child.__qwe__, 10)
