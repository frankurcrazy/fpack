#!/usr/bin/env python

""" fpack basic field types

    fpack includes field support for primitive types, string
    and bytes
"""

import struct

from fpack.utils import get_length


class Field:
    def __init__(self, val=None):
        self.val = val

    def pack(self):
        raise NotImplementedError

    def unpack(self, data):
        raise NotImplementedError

    @classmethod
    def from_bytes(cls, data):
        obj = cls()
        length = obj.unpack(data)

        return (obj, length)

    @property
    def size(self):
        raise NotImplementedError

    def __repr__(self):
        return f"{self.val}"


class Primitive(Field):
    STRUCT = struct.Struct("!I")

    def __init__(self, val=0):
        super().__init__(val)

    def pack(self) -> bytes:
        return self.STRUCT.pack(self.val)

    def unpack(self, data):
        length = get_length(data)
        if length < self.STRUCT.size:
            raise ValueError(f"size too small: {length}")

        self.val = self.STRUCT.unpack(data[: self.STRUCT.size])[0]

        return self.STRUCT.size

    @property
    def size(self):
        return self.STRUCT.size


class Int64(Primitive):
    STRUCT = struct.Struct("!q")


class Uint64(Primitive):
    STRUCT = struct.Struct("!Q")


class Int32(Primitive):
    STRUCT = struct.Struct("!i")


class Uint32(Primitive):
    STRUCT = struct.Struct("!I")


class Int16(Primitive):
    STRUCT = struct.Struct("!h")


class Uint16(Primitive):
    STRUCT = struct.Struct("!H")


class Int8(Primitive):
    STRUCT = struct.Struct("b")


class Uint8(Primitive):
    STRUCT = struct.Struct("B")


class Float(Primitive):
    STRUCT = struct.Struct("!f")


class Double(Primitive):
    STRUCT = struct.Struct("!d")


class Bytes(Field):
    LENGTH_STRUCT = struct.Struct("!H")

    def __init__(self, val=b""):
        super().__init__(val)

    def pack(self):
        length = get_length(self.val)
        lengthBytes = self.LENGTH_STRUCT.pack(length)
        if self.val:
            return lengthBytes + bytes(self.val)

        return lengthBytes

    def unpack(self, data):
        length = get_length(data)

        if length < self.LENGTH_STRUCT.size:
            raise ValueError(f"size too short: {length}.")

        payload_length = self.LENGTH_STRUCT.unpack(data[: self.LENGTH_STRUCT.size])[0]

        if length < self.LENGTH_STRUCT.size + payload_length:
            raise ValueError(f"incomplete field, size too short: {length}.")

        self.val = data[
            self.LENGTH_STRUCT.size : self.LENGTH_STRUCT.size + payload_length
        ]

        return self.LENGTH_STRUCT.size + payload_length

    @property
    def size(self):
        return self.LENGTH_STRUCT.size + get_length(self.val)


class String(Field):
    LENGTH_STRUCT = struct.Struct("!H")

    def __init__(self, val=""):
        super().__init__(val)

    def pack(self):
        length = get_length(self.val)
        lengthBytes = self.LENGTH_STRUCT.pack(length)

        if self.val:
            return lengthBytes + self.val.encode("utf-8")

        return lengthBytes

    def unpack(self, data):
        length = get_length(data)

        if length < self.LENGTH_STRUCT.size:
            raise ValueError(f"size too short: {length}.")

        payload_length = self.LENGTH_STRUCT.unpack(data[: self.LENGTH_STRUCT.size])[0]

        if length < self.LENGTH_STRUCT.size + payload_length:
            raise ValueError(f"incomplete field, size too short: {length}.")

        self.val = bytes(
            data[self.LENGTH_STRUCT.size : self.LENGTH_STRUCT.size + payload_length]
        ).decode("utf-8")

        return self.LENGTH_STRUCT.size + payload_length

    @property
    def size(self):
        return self.LENGTH_STRUCT.size + get_length(self.val)

    def __repr__(self):
        if self.val is None:
            return f"{self.val}"
        return f'"{self.val}"'


def field_factory(name, type_):
    """ field type factory

        This function generate custom field classes for
        designated types.

        Arguments:
            name (str): name of the class
            type (class): class from which the custom field class
                          inherit

        Return:
            field class
    """
    return type(name, (type_,), {})


__all__ = [
    "Field",
    "Uint8",
    "Uint16",
    "Uint32",
    "Uint64",
    "Int8",
    "Int16",
    "Int32",
    "Int64",
    "Bytes",
    "String",
    "field_factory",
]
