class Field:
    value = None

    def __get__(self, instance, owner):
        return self.value


class TextField(Field):
    pass


class NumberField(Field):
    pass


class Model(object):

    @classmethod
    def resolve_fields(cls):
        fields = []
        for name, obj in cls.__dict__.items():
            if isinstance(obj, Field):
                fields.append((name, obj))
        return fields

    def get_values(self):
        values = {}
        for field_name, field_obj in self.resolve_fields():
            values[field_name] = self.__getattribute__(field_name)
        return values
