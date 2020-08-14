#!/usr/bin/env python

import struct
from io import BytesIO
from fpack.utils import get_length

class Message:
    Fields = []

    def __init__(self, *args, **kwargs):
        # Initialize fields
        self._fields = [field() for field in self.Fields]
        self._field_names = [field.__name__ for field in self.Fields]

        for k in kwargs.keys():
            if k in self._field_names:
                self.__setattr__(k, kwargs[k])

    def pack(self) -> bytes:
        payload = BytesIO()

        for field in self._fields:
            payload.write(field.pack())

        return payload.getvalue()

    def unpack(self, data):
        self._fields = []

        offset = 0
        for field in self.Fields:
            f, processed = field.from_bytes(data[offset:])
            self._fields.append(f)
            offset += processed

        return offset

    @classmethod
    def from_bytes(cls, data):
        obj = cls()
        length = obj.unpack(data)

        return (obj, length)

    def __repr__(self):
        fields_str = ' '.join(f'{field.__class__.__name__}={str(field)}' for field in self._fields)
        return f"<{self.__class__.__name__} {fields_str}>"

    def __getattr__(self, attr):
        try:
            idx = self._field_names.index(attr)

            if isinstance(self._fields[idx], Message):
                return self._fields[idx]

            return self._fields[idx].val

        except ValueError:
            return None

    def __setattr__(self, attr, val):
        if attr in ['_field_names', '_fields']:
            object.__setattr__(self, attr, val)
            return

        try:
            idx = self._field_names.index(attr)
            self._fields[idx].val = val
        except ValueError:
            object.__setattr__(self, attr, val)

    @property
    def size(self):
        return sum([field.size for field in self._fields])

__all__ = ["Message"]
