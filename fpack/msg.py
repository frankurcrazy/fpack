#!/usr/bin/env python

import struct
from io import BytesIO
from fpack.utils import get_length

class Message:
    Fields = []

    def __init__(self):
        # Initialize fields
        self._fields = [field() for field in self.Fields]
        self._field_names = [field.__name__ for filed in self.Fields]

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

    def __repr__(self):
        return f"<{self.__class__.__name__} {' '.join(str(field) for field in self._fields)}>"

    def __getattr__(self, attr):
        try:
            idx = self._field_names.index(attr)
            return self._fields[idx].val

        except ValueError:
            return None

    def __setattr__(self, attr, val):
        try:
            idx = self._field_names.index(attr)
            self._fields[idx].val = val
        except ValueError:
            object.__setattr__(self, attr, val)

__all__ = ["Message"]
