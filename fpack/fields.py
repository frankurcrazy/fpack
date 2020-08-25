#!/usr/bin/env python

""" fpack basic field types

    fpack includes field support for primitive types, string
    and bytes
"""

import struct
from io import BytesIO

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
        try:
            self.val = self.STRUCT.unpack(data[: self.STRUCT.size])[0]
        except struct.error:
            raise ValueError(
                f"size too small: {get_length(data)}, expect {self.STRUCT.size}."
            )

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
        data = memoryview(data)

        length = get_length(data)

        try:
            payload_length = self.LENGTH_STRUCT.unpack(data[: self.LENGTH_STRUCT.size])[
                0
            ]
        except struct.error:
            raise ValueError(f"size too short: {get_length(data)}.")

        if length < self.LENGTH_STRUCT.size + payload_length:
            raise ValueError(f"incomplete field, size too short: {length}.")

        self.val = data[
            self.LENGTH_STRUCT.size : self.LENGTH_STRUCT.size + payload_length
        ].tobytes()

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


class Array(Field):
    def __init__(self, val=[]):
        super().__init__(val=val)

    def __repr__(self):
        item_str = ",".join(str(x) for x in self.val)
        item_str = f"[{item_str}]"

        return f"<{self.__class__.__name__} length={get_length(self.val)} items={item_str}>"


def array_field_factory(name, type_):
    array_length_struct = struct.Struct("!H")

    @property
    def size(self):
        total_size = array_length_struct.size
        for v in self.val:
            total_size += v.size

        return total_size

    def len_(self):
        return get_length(self.val)

    def pack(self):
        buf = BytesIO()
        buf.write(array_length_struct.pack(get_length(self.val)))

        payload_size = array_length_struct.size
        for v in self.val:
            if not isinstance(v, type_):
                raise TypeError(f"Incompatible type {v.__class__.__name__}.")
            buf.write(v.pack())
            payload_size += v.size

        return buf.getvalue()

    def unpack(self, data):
        data = memoryview(data)

        self.val = []
        offset = 0

        try:
            array_length, *_ = array_length_struct.unpack(
                data[0 : array_length_struct.size]
            )
            offset += array_length_struct.size
        except struct.error:
            raise ValueError(f"incomplete field, size too small: {get_length(data)}.")

        for _ in range(array_length):
            unpacked, len_ = type_.from_bytes(data[offset:])
            self.val.append(unpacked)
            offset += len_

        return (self, offset)

    return type(
        name,
        (Array,),
        {
            "pack": pack,
            "unpack": unpack,
            "__len__": len_,
            "size": size,
            "__slots__": ("val",),
        },
    )


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
    return type(name, (type_,), {"__slots__": ("val",)})


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
    "Array",
    "field_factory",
    "array_field_factory",
]
