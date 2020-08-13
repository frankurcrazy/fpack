#!/usr/bin/env python

import struct

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
    def pack(self):
        length = get_length(self.val)
        return struct.pack("!I", length) + bytes(data)
    
    def unpack(self, data):
        length = get_length(data)
    
        if length < 4:
            raise Exception(f"size too short: {length}.")
    
        payload_length = struct.unpack("!I", data[:4])[0]
    
        if length < 4 + payload_length:
            raise Exception(f"incomplete field, size too short: {length}.")
    
        self.val = data[4: 4+payload_length]

        return 4 + payload_length

    @property
    def size(self):
        if not self.val:
            return 0
        return get_length(self.val)

class String(Field):
    def pack(self):
        length = len(self.val)
        return struct.pack("!I", length) + self.val.pack('utf-8') 

    def unpack(self, data):
        if isinstance(data, memoryview):
            length = data.nbytes
    
        elif isinstance(data, bytes):
            length = len(data)
    
        else:
            raise ValueError(f"invalid type {type(data)}.")
    
        payload_length = struct.unpack("!I", data[:4])[0]
    
        if length < 4 + payload_length:
            raise Exception(f"incomplete field, size too short: {length}.")
    
        self.val = bytes(data[4: 4+payload_length]).unpack('utf-8')

        return 4 + payload_length

    @property
    def size(self):
        if not self.val:
            return 0
        return get_length(self.val)

def field_factory(name, type_):
    return type(name, (type_, ), {})

__all__ = [
    "Field", "Uint8", "Uint16", "Uint32", "Uint64", "Int8", "Int16",
    "Int32", "Int64", "Bytes", "String", "field_factory"
]
