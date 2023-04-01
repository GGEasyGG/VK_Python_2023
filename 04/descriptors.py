import re


class EmailAddressDescriptor:
    def __set_name__(self, owner, name):
        self.name = f'{name}_email_field'

    def __set__(self, instance, value):
        if instance is None:
            return

        if isinstance(value, str) and re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            return setattr(instance, self.name, value)
        else:
            raise ValueError(f"{self.name} must be a valid email address")

    def __get__(self, instance, cls=None):
        if instance is None:
            return

        return getattr(instance, self.name)

    def __delete__(self, instance):
        if instance is None:
            return

        return delattr(instance, self.name)


class PhoneNumberDescriptor:
    def __set_name__(self, owner, name):
        self.name = f'{name}_phone_number_field'

    def __set__(self, instance, value):
        if instance is None:
            return

        if isinstance(value, str) and (re.match(r"^\+7\s?\(\d{3}\)\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}$", value) or
                                       re.match(r"^\+7\s?\d{3}\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}$", value)):
            return setattr(instance, self.name, value)
        else:
            raise ValueError(f"{self.name} must be a valid russian phone number")

    def __get__(self, instance, cls=None):
        if instance is None:
            return

        return getattr(instance, self.name)

    def __delete__(self, instance):
        if instance is None:
            return

        return delattr(instance, self.name)


class GenderDescriptor:
    def __set_name__(self, owner, name):
        self.name = f'{name}_gender_field'

    def __set__(self, instance, value):
        if instance is None:
            return

        if value in ["Male", "Female"]:
            return setattr(instance, self.name, value)
        else:
            raise ValueError(f"{self.name} must be 'Male' or 'Female'")

    def __get__(self, instance, cls=None):
        if instance is None:
            return

        return getattr(instance, self.name)

    def __delete__(self, instance):
        if instance is None:
            return

        return delattr(instance, self.name)
