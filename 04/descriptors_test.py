import unittest
from descriptors import EmailAddressDescriptor, GenderDescriptor, PhoneNumberDescriptor


class TestDescriptors(unittest.TestCase):
    def setUp(self):
        class Person:
            email = EmailAddressDescriptor()
            phone = PhoneNumberDescriptor()
            gender = GenderDescriptor()

        self.person = Person()

    def test_email_address_descriptor_valid_email(self):
        self.person.email = "test@example.com"
        self.assertEqual(self.person.email, "test@example.com")
        self.assertTrue(hasattr(self.person, 'email_email_field'))

        self.person.email = "Test_123%HJ.HKJ@eXa.mp21e.cOm"
        self.assertEqual(self.person.email, "Test_123%HJ.HKJ@eXa.mp21e.cOm")
        self.assertTrue(hasattr(self.person, 'email_email_field'))

    def test_email_address_descriptor_invalid_email(self):
        with self.assertRaises(ValueError) as err:
            self.person.email = "test@example"

        self.assertEqual(str(err.exception), 'email_email_field must be a valid email address')

        with self.assertRaises(ValueError) as err:
            self.person.email = 123

        self.assertEqual(str(err.exception), 'email_email_field must be a valid email address')

        with self.assertRaises(ValueError) as err:
            self.person.email = None

        self.assertEqual(str(err.exception), 'email_email_field must be a valid email address')

        with self.assertRaises(ValueError) as err:
            self.person.email = "testexample.ru"

        self.assertEqual(str(err.exception), 'email_email_field must be a valid email address')

        with self.assertRaises(ValueError) as err:
            self.person.email = "te:st@exam#ple.c1o"

        self.assertEqual(str(err.exception), 'email_email_field must be a valid email address')

    def test_phone_number_descriptor_valid_phone_number(self):
        self.person.phone = "+7(123)456-78-90"
        self.assertEqual(self.person.phone, "+7(123)456-78-90")
        self.assertTrue(hasattr(self.person, 'phone_phone_number_field'))

        self.person.phone = "+7 (123) 456-78-90"
        self.assertEqual(self.person.phone, "+7 (123) 456-78-90")
        self.assertTrue(hasattr(self.person, 'phone_phone_number_field'))

        self.person.phone = "+7 123 456-78-90"
        self.assertEqual(self.person.phone, "+7 123 456-78-90")
        self.assertTrue(hasattr(self.person, 'phone_phone_number_field'))

        self.person.phone = "+7 123 456 78 90"
        self.assertEqual(self.person.phone, "+7 123 456 78 90")
        self.assertTrue(hasattr(self.person, 'phone_phone_number_field'))

        self.person.phone = "+71234567890"
        self.assertEqual(self.person.phone, "+71234567890")
        self.assertTrue(hasattr(self.person, 'phone_phone_number_field'))

    def test_phone_number_descriptor_invalid_phone_number(self):
        with self.assertRaises(ValueError) as err:
            self.person.phone = 123

        self.assertEqual(str(err.exception), 'phone_phone_number_field must be a valid russian phone number')

        with self.assertRaises(ValueError) as err:
            self.person.phone = None

        self.assertEqual(str(err.exception), 'phone_phone_number_field must be a valid russian phone number')

        with self.assertRaises(ValueError) as err:
            self.person.phone = "1234567890"

        self.assertEqual(str(err.exception), 'phone_phone_number_field must be a valid russian phone number')

        with self.assertRaises(ValueError) as err:
            self.person.phone = "+1 234 567 89 00"

        self.assertEqual(str(err.exception), 'phone_phone_number_field must be a valid russian phone number')

        with self.assertRaises(ValueError) as err:
            self.person.phone = "+72345678"

        self.assertEqual(str(err.exception), 'phone_phone_number_field must be a valid russian phone number')

        with self.assertRaises(ValueError) as err:
            self.person.phone = "+723456789056567578"

        self.assertEqual(str(err.exception), 'phone_phone_number_field must be a valid russian phone number')

        with self.assertRaises(ValueError) as err:
            self.person.phone = "+7(1234567890"

        self.assertEqual(str(err.exception), 'phone_phone_number_field must be a valid russian phone number')

        with self.assertRaises(ValueError) as err:
            self.person.phone = "+7123)4567890"

        self.assertEqual(str(err.exception), 'phone_phone_number_field must be a valid russian phone number')

        with self.assertRaises(ValueError) as err:
            self.person.phone = "+7(123456) 78-90"

        self.assertEqual(str(err.exception), 'phone_phone_number_field must be a valid russian phone number')

        with self.assertRaises(ValueError) as err:
            self.person.phone = "+7 1234 5678 90"

        self.assertEqual(str(err.exception), 'phone_phone_number_field must be a valid russian phone number')

        with self.assertRaises(ValueError) as err:
            self.person.phone = "+7 12-34-56-78-90"

        self.assertEqual(str(err.exception), 'phone_phone_number_field must be a valid russian phone number')

    def test_gender_descriptor_valid_gender(self):
        self.person.gender = "Male"
        self.assertEqual(self.person.gender, "Male")
        self.assertTrue(hasattr(self.person, 'gender_gender_field'))

        self.person.gender = "Female"
        self.assertEqual(self.person.gender, "Female")
        self.assertTrue(hasattr(self.person, 'gender_gender_field'))

    def test_gender_descriptor_invalid_gender(self):
        with self.assertRaises(ValueError) as err:
            self.person.gender = "Other"

        self.assertEqual(str(err.exception), "gender_gender_field must be 'Male' or 'Female'")

        with self.assertRaises(ValueError) as err:
            self.person.gender = 123

        self.assertEqual(str(err.exception), "gender_gender_field must be 'Male' or 'Female'")

        with self.assertRaises(ValueError) as err:
            self.person.gender = None

        self.assertEqual(str(err.exception), "gender_gender_field must be 'Male' or 'Female'")

    def test_email_address_descriptor_delete_value(self):
        self.person.email = "test@example.com"
        self.assertTrue(hasattr(self.person, 'email_email_field'))
        del self.person.email
        self.assertFalse(hasattr(self.person, 'email_email_field'))

    def test_phone_number_descriptor_delete_value(self):
        self.person.phone = "+7 (123) 456-78-90"
        self.assertTrue(hasattr(self.person, 'phone_phone_number_field'))
        del self.person.phone
        self.assertFalse(hasattr(self.person, 'phone_phone_number_field'))

    def test_gender_descriptor_delete_value(self):
        self.person.gender = "Male"
        self.assertTrue(hasattr(self.person, 'gender_gender_field'))
        del self.person.gender
        self.assertFalse(hasattr(self.person, 'gender_gender_field'))

    def test_email_address_descriptor_wrong_instance(self):
        desc = EmailAddressDescriptor()

        self.assertIsNone(desc.__set__(None, "test@example.com"))
        self.assertIsNone(desc.__get__(None))
        self.assertIsNone(desc.__delete__(None))

    def test_phone_number_descriptor_wrong_instance(self):
        desc = PhoneNumberDescriptor()

        self.assertIsNone(desc.__set__(None, "+7 (123) 456-78-90"))
        self.assertIsNone(desc.__get__(None))
        self.assertIsNone(desc.__delete__(None))

    def test_gender_descriptor_wrong_instance(self):
        desc = GenderDescriptor()

        self.assertIsNone(desc.__set__(None, "Male"))
        self.assertIsNone(desc.__get__(None))
        self.assertIsNone(desc.__delete__(None))
