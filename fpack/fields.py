#!/usr/bin/env python

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
        return f"{self.__class__.__name__}={self.val}"

class Primative(Field):
    STRUCT = struct.Struct("!I")

    def pack(self) -> bytes:
        return self.STRUCT.pack(self.val)
    
    def unpack(self, data):
        length = get_length(data)
        if length < self.STRUCT.size:
            raise ValueError(f"size too small: {length}")

        self.val = self.STRUCT.unpack(data[:self.STRUCT.size])[0]

        return self.STRUCT.size

    @property
    def size(self):
        return self.STRUCT.size

class Int64(Primative):
    STRUCT = struct.Struct("!l")

class Uint64(Primative):
    STRUCT = struct.Struct("!L")

class Int32(Primative):
    STRUCT = struct.Struct("!i")

class Uint32(Primative):
    STRUCT = struct.Struct("!I")

class Int16(Primative):
    STRUCT = struct.Struct("!h")

class Uint16(Primative):
    STRUCT = struct.Struct("!H")

class Int8(Primative):
    STRUCT = struct.Struct("b")

class Uint8(Primative):
    STRUCT = struct.Struct("B")

class Float(Primative):
    STRUCT = struct.Struct("!f")

class Double(Primative):
    STRUCT = struct.Struct("!d")

class Bytes(Field):
    LENGTH_STRUCT = struct.Struct("!H")

    def pack(self):
        length = get_length(self.val)
        return self.LENGTH_STRUCT.pack(length) + bytes(data)
    
    def unpack(self, data):
        length = get_length(data)
    
        if length < self.LENGTH_STRUCT.size:
            raise Exception(f"size too short: {length}.")
    
        payload_length = struct.unpack("!I", data[:self.LENGTH_STRUCT.size])[0]
    
        if length < self.LENGTH_STRUCT.size + payload_length:
            raise Exception(f"incomplete field, size too short: {length}.")
    
        self.val = data[self.LENGTH_STRUCT.size: self.LENGTH_STRUCT.size+payload_length]

        return self.LENGTH_STRUCT.size + payload_length

    @property
    def size(self):
        return self.LENGTH_STRUCT.size + get_length(self.val)

class String(Field):
    LENGTH_STRUCT = struct.Struct("!H")

    def pack(self):
        length = len(self.val)
        return self.LENGTH_STRUCT.pack(length) + self.val.encode('utf-8') 

    def unpack(self, data):
        if isinstance(data, memoryview):
            length = data.nbytes
    
        elif isinstance(data, bytes):
            length = len(data)
    
        else:
            raise ValueError(f"invalid type {type(data)}.")
    
        payload_length = self.LENGTH_STRUCT.unpack(data[:self.LENGTH_STRUCT.size])[0]
    
        if length < self.LENGTH_STRUCT.size + payload_length:
            raise Exception(f"incomplete field, size too short: {length}.")
    
        self.val = bytes(data[self.LENGTH_STRUCT.size: self.LENGTH_STRUCT.size+payload_length]).decode('utf-8')

        return self.LENGTH_STRUCT.size + payload_length

    @property
    def size(self):
        return self.LENGTH_STRUCT.size + get_length(self.val)

    def __repr__(self):
        return f"{self.__class__.__name__}=\"{self.val}\""

def field_factory(name, type_):
    return type(name, (type_, ), {})

__all__ = [
    "Field", "Uint8", "Uint16", "Uint32", "Uint64", "Int8", "Int16",
    "Int32", "Int64", "Bytes", "String", "field_factory"
]
