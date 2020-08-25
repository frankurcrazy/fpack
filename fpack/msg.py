#!/usr/bin/env python

from collections import OrderedDict
from io import BytesIO


class Message:
    """ Message

        Message is the base class of all custom messages. It implements general methods
        for all messages.
    """

    Fields = []

    def __init__(self, *_, **kwargs):
        # Initialize fields
        self._fields = OrderedDict()
        for field in self.Fields:
            if field.__name__ in kwargs:
                obj = field(kwargs[field.__name__])
            else:
                obj = field()

            self._fields[field.__name__] = obj

    def pack(self) -> bytes:
        payload = BytesIO()

        for _, v in self._fields.items():
            payload.write(v.pack())

        return payload.getvalue()

    def unpack(self, data):
        offset = 0
        for k, v in self._fields.items():
            processed = v.unpack(data[offset:])
            offset += processed

        return offset

    @classmethod
    def from_bytes(cls, data):
        obj = cls()
        length = obj.unpack(data)
        return (obj, length)

    def __repr__(self):
        fields_str = " ".join(f"{k}={str(v)}" for k, v in self._fields)
        return f"<{self.__class__.__name__} {fields_str}>"

    def __getattr__(self, attr):
        try:
            field = self._fields[attr]

            if isinstance(field, Message):
                return field

            return field.val

        except KeyError:
            return None

    def __setattr__(self, attr, val):
        if attr == "_fields":
            object.__setattr__(self, attr, val)
            return

        if attr in self._fields:
            self._fields[attr].val = val
        else:
            object.__setattr__(self, attr, val)

    @property
    def size(self):
        return sum([field.size for field in self._fields])


__all__ = ["Message"]
