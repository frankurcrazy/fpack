#!/usr/bin/env python

import struct
import unittest

try:
    from fpack import *
except ImportError:
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(".", "..")))
    from fpack import *


class TestField(unittest.TestCase):
    def test_not_implemented_methods(self):
        field = Field()

        with self.assertRaises(NotImplementedError):
            field.pack()

        with self.assertRaises(NotImplementedError):
            field.unpack(b"12345")

        with self.assertRaises(NotImplementedError):
            field.size

        with self.assertRaises(NotImplementedError):
            field = Field.from_bytes(b"12345")

    def test_str_representation(self):
        self.assertEqual(str(Field()), "None")
        self.assertEqual(str(Field(1234)), "1234")


class TestPrimitiveFieldPack(unittest.TestCase):
    def test_uint8_pack(self):
        s = struct.Struct("B")
        val = 255
        f = Uint8(val)
        p = f.pack()

        self.assertEqual(len(p), s.size)
        self.assertEqual(p, s.pack(val))

    def test_uint16_pack(self):
        s = struct.Struct("!H")
        val = 65535
        f = Uint16(val)
        p = f.pack()

        self.assertEqual(len(p), s.size)
        self.assertEqual(p, s.pack(val))

    def test_uint32_pack(self):
        s = struct.Struct("!I")
        val = 12345789
        f = Uint32(val)
        p = f.pack()

        self.assertEqual(len(p), s.size)
        self.assertEqual(p, s.pack(val))

    def test_uint64_pack(self):
        s = struct.Struct("!Q")
        val = 2555555555
        f = Uint64(val)
        p = f.pack()

        self.assertEqual(f.size, s.size)
        self.assertEqual(len(p), s.size)
        self.assertEqual(p, s.pack(val))

    def test_int8_pack(self):
        s = struct.Struct("b")
        val = -128
        f = Int8(val)
        p = f.pack()

        self.assertEqual(f.size, s.size)
        self.assertEqual(len(p), s.size)
        self.assertEqual(p, s.pack(val))

    def test_int16_pack(self):
        s = struct.Struct("!h")
        val = -32767
        f = Int16(val)
        p = f.pack()

        self.assertEqual(f.size, s.size)
        self.assertEqual(len(p), s.size)
        self.assertEqual(p, s.pack(val))

    def test_int32_pack(self):
        s = struct.Struct("!i")
        val = -12345789
        f = Int32(val)
        p = f.pack()

        self.assertEqual(f.size, s.size)
        self.assertEqual(len(p), s.size)
        self.assertEqual(p, s.pack(val))

    def test_int64_pack(self):
        s = struct.Struct("!q")
        val = -2055555555
        f = Int64(val)
        p = f.pack()

        self.assertEqual(f.size, s.size)
        self.assertEqual(len(p), s.size)
        self.assertEqual(p, s.pack(val))


class TestPrimitiveFieldUnpack(unittest.TestCase):
    def test_uint8_unpack(self):
        s = struct.Struct("B")
        val = 255
        f = Uint8()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

        p, length = Uint8.from_bytes(s.pack(val))
        self.assertTrue(isinstance(p, Uint8))
        self.assertEqual(length, s.size)
        self.assertEqual(p.val, val)

    def test_uint16_unpack(self):
        s = struct.Struct("!H")
        val = 65535
        f = Uint16()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

        p, length = Uint16.from_bytes(s.pack(val))
        self.assertTrue(isinstance(p, Uint16))
        self.assertEqual(length, s.size)
        self.assertEqual(p.val, val)

    def test_uint32_unpack(self):
        s = struct.Struct("!I")
        val = 12345789
        f = Uint32()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

        p, length = Uint32.from_bytes(s.pack(val))
        self.assertTrue(isinstance(p, Uint32))
        self.assertEqual(length, s.size)
        self.assertEqual(p.val, val)

    def test_uint64_unpack(self):
        s = struct.Struct("!Q")
        val = 2555555555
        f = Uint64()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

        p, length = Uint64.from_bytes(s.pack(val))
        self.assertTrue(isinstance(p, Uint64))
        self.assertEqual(length, s.size)
        self.assertEqual(p.val, val)

    def test_int8_unpack(self):
        s = struct.Struct("b")
        val = -128
        f = Int8()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

        p, length = Int8.from_bytes(s.pack(val))
        self.assertTrue(isinstance(p, Int8))
        self.assertEqual(length, s.size)
        self.assertEqual(p.val, val)

    def test_int16_unpack(self):
        s = struct.Struct("!h")
        val = -32767
        f = Int16()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

        p, length = Int16.from_bytes(s.pack(val))
        self.assertTrue(isinstance(p, Int16))
        self.assertEqual(length, s.size)
        self.assertEqual(p.val, val)

    def test_int32_unpack(self):
        s = struct.Struct("!i")
        val = -12345789
        f = Int32()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

        p, length = Int32.from_bytes(s.pack(val))
        self.assertTrue(isinstance(p, Int32))
        self.assertEqual(length, s.size)
        self.assertEqual(p.val, val)

    def test_int64_unpack(self):
        s = struct.Struct("!q")
        val = -2055555555
        f = Int64()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

        p, length = Int64.from_bytes(s.pack(val))
        self.assertTrue(isinstance(p, Int64))
        self.assertEqual(length, s.size)
        self.assertEqual(p.val, val)

    def test_uint8_unpack_undersize(self):
        s = struct.Struct("B")
        val = 255
        f = Uint8()

        with self.assertRaises(ValueError):
            p = f.unpack(s.pack(val)[:0])

    def test_uint16_unpack_undersize(self):
        s = struct.Struct("!H")
        val = 65535
        f = Uint16()

        with self.assertRaises(ValueError):
            p = f.unpack(s.pack(val)[:0])

    def test_uint32_unpack_undersize(self):
        s = struct.Struct("!I")
        val = 12345789
        f = Uint32()

        with self.assertRaises(ValueError):
            p = f.unpack(s.pack(val)[:0])

    def test_uint64_unpack_undersize(self):
        s = struct.Struct("!Q")
        val = 2555555555
        f = Uint64()

        with self.assertRaises(ValueError):
            p = f.unpack(s.pack(val)[:0])

    def test_int8_unpack_undersize(self):
        s = struct.Struct("b")
        val = -128
        f = Int8()

        with self.assertRaises(ValueError):
            p = f.unpack(s.pack(val)[:0])

    def test_int16_unpack_undersize(self):
        s = struct.Struct("!h")
        val = -32767
        f = Int16()

        with self.assertRaises(ValueError):
            p = f.unpack(s.pack(val)[:1])

    def test_int32_unpack_undersize(self):
        s = struct.Struct("!i")
        val = -12345789
        f = Int32()

        with self.assertRaises(ValueError):
            p = f.unpack(s.pack(val)[:3])

    def test_int64_unpack_undersize(self):
        s = struct.Struct("!q")
        val = -2055555555
        f = Int64()

        with self.assertRaises(ValueError):
            p = f.unpack(s.pack(val)[:5])


class TestStringField(unittest.TestCase):
    def test_pack_string(self):
        val = "helloworld!"
        field = String(val)
        packed = field.pack()
        test_packed = struct.pack("!H", len(val)) + val.encode("utf-8")

        self.assertEqual(packed, test_packed)
        self.assertEqual(field.size, len(test_packed))

    def test_pack_string_empty(self):
        val = ""
        field = String(val)
        packed = field.pack()
        test_packed = struct.pack("!H", len(val)) + val.encode("utf-8")

        self.assertEqual(packed, test_packed)
        self.assertEqual(field.size, len(test_packed))

    def test_pack_string_none(self):
        val = None
        field = String(val)
        packed = field.pack()

        self.assertEqual(str(field), "None")
        self.assertEqual(packed, b"\x00" * 2)

    def test_unpack_string(self):
        val = "helloworld!"
        test_packed = struct.pack("!H", len(val)) + val.encode("utf-8")

        unpacked, length = String.from_bytes(test_packed)
        self.assertEqual(unpacked.val, val)
        self.assertEqual(unpacked.size, len(test_packed))
        self.assertEqual(str(unpacked), f'"{val}"')

    def test_unpack_string_undersized(self):
        val = "helloworld!"
        test_packed = struct.pack("!H", len(val)) + val.encode("utf-8")

        with self.assertRaises(ValueError):
            unpacked, length = String.from_bytes(test_packed[:-1])

        with self.assertRaises(ValueError):
            unpacked, length = String.from_bytes(test_packed[:1])

    def test_unpack_string_oversized(self):
        val = "helloworld!"
        test_packed = struct.pack("!H", len(val)) + val.encode("utf-8")
        sth = b"testdata123"

        unpacked, length = String.from_bytes(test_packed + sth)
        self.assertEqual(unpacked.val, val)
        self.assertEqual(unpacked.size, len(test_packed))


class TestBytesField(unittest.TestCase):
    def test_pack_bytes(self):
        val = b"helloworld!"
        field = Bytes(val)
        packed = field.pack()
        test_packed = struct.pack("!H", len(val)) + val

        self.assertEqual(packed, test_packed)
        self.assertEqual(field.size, len(test_packed))

    def test_pack_bytes_empty(self):
        val = b""
        field = Bytes(val)
        packed = field.pack()
        test_packed = struct.pack("!H", len(val)) + val

        self.assertEqual(packed, test_packed)
        self.assertEqual(field.size, len(test_packed))

    def test_pack_bytes_none(self):
        val = None
        field = Bytes(val)
        packed = field.pack()

        self.assertEqual(str(field), "None")
        self.assertEqual(packed, b"\x00" * 2)

    def test_unpack_bytes(self):
        val = b"helloworld!"
        test_packed = struct.pack("!H", len(val)) + val

        unpacked, length = Bytes.from_bytes(test_packed)
        self.assertEqual(unpacked.val, val)
        self.assertEqual(unpacked.size, len(test_packed))
        self.assertEqual(str(unpacked), f"{val}")

    def test_unpack_bytes_undersized(self):
        val = b"helloworld!"
        test_packed = struct.pack("!H", len(val)) + val

        with self.assertRaises(ValueError):
            unpacked, length = Bytes.from_bytes(test_packed[:-1])

        with self.assertRaises(ValueError):
            unpacked, length = Bytes.from_bytes(test_packed[:1])

    def test_unpack_bytes_oversized(self):
        val = b"helloworld!"
        test_packed = struct.pack("!H", len(val)) + val
        sth = b"testdata123"

        unpacked, length = Bytes.from_bytes(test_packed + sth)
        self.assertEqual(unpacked.val, val)
        self.assertEqual(unpacked.size, len(test_packed))


class TestArrayField(unittest.TestCase):
    def test_pack_string_array(self):
        array_of_string = [
            String("this"),
            String("is"),
            String("an"),
            String("array"),
            String("of"),
            String("strings."),
        ]

        StringArray = array_field_factory("StringArray", String)
        array = StringArray(array_of_string)
        item_strings = f"[{','.join(str(x) for x in array_of_string)}]"
        packed = b"\x00\x06"

        for s in array_of_string:
            packed += s.pack()

        self.assertEqual(len(array), len(array_of_string))
        self.assertEqual(array.size, 37)
        self.assertEqual(
            str(array),
            f"<StringArray length={len(array_of_string)} items={item_strings}>",
        )
        self.assertEqual(array.pack(), packed)

    def test_pack_string_array_incompatible_size(self):
        array_of_string = [
            String("this"),
            String("is"),
            String("an"),
            String("array"),
            String("of"),
            Bytes(b"strings."),
        ]

        StringArray = array_field_factory("StringArray", String)
        with self.assertRaises(TypeError):
            array = StringArray(array_of_string)
            array.pack()

    def test_unpack_string_array(self):
        StringArray = array_field_factory("StringArray", String)

        raw = b"\x00\x06\x00\x04this\x00\x02is\x00\x02an\x00\x05array\x00\x02of\x00\x08strings."
        unpacked, s = StringArray.from_bytes(raw)

        self.assertTrue(unpacked.size, len(raw))
        self.assertEqual(s, len(raw))
        self.assertTrue(len(unpacked), 6)

    def test_unpack_string_array_undersized(self):
        StringArray = array_field_factory("StringArray", String)

        raw = b"\x00\x06\x00\x04this\x00\x02is\x00\x02an\x00\x05array\x00\x02of\x00\x08strings."
        with self.assertRaises(ValueError):
            unpacked, s = StringArray.from_bytes(raw[:0])

    def test_unpack_string_array_incomplete(self):
        StringArray = array_field_factory("StringArray", String)

        raw = b"\x00\x06\x00\x04this\x00\x02is\x00\x02an\x00\x05array\x00\x02of\x00\x08strings."
        with self.assertRaises(ValueError):
            unpacked, s = StringArray.from_bytes(raw[:-1])


class TestFieldFactory(unittest.TestCase):
    def test_field_factory(self):
        fieldClass = field_factory("Test", Uint8)

        self.assertEqual(fieldClass.__name__, "Test")
        self.assertTrue(issubclass(fieldClass, Uint8))

    def test_array_field_factory(self):
        fieldClass = array_field_factory("TestArray", Uint8)

        self.assertEqual(fieldClass.__name__, "TestArray")
        self.assertTrue(issubclass(fieldClass, Array))


if __name__ == "__main__":
    unittest.main()
