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
        for field in self.resolve_fields():
            values[field[0]] = field[1].value
        return values