#!/usr/bin/env python

import unittest
import struct

try:
    from fpack import *
except ImportError:
    import os, sys
    sys.path.append(
        os.path.abspath(os.path.join('.', '..')))
    from fpack import *

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

    def test_uint16_unpack(self):
        s = struct.Struct("!H")
        val = 65535
        f = Uint16()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

    def test_uint32_unpack(self):
        s = struct.Struct("!I")
        val = 12345789
        f = Uint32()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

    def test_uint64_unpack(self):
        s = struct.Struct("!Q")
        val = 2555555555
        f = Uint64()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

    def test_int8_unpack(self):
        s = struct.Struct("b")
        val = -128
        f = Int8()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

    def test_int16_unpack(self):
        s = struct.Struct("!h")
        val = -32767
        f = Int16()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

    def test_int32_unpack(self):
        s = struct.Struct("!i")
        val = -12345789
        f = Int32()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

    def test_int64_unpack(self):
        s = struct.Struct("!q")
        val = -2055555555
        f = Int64()
        p = f.unpack(s.pack(val))

        self.assertEqual(p, s.size)
        self.assertEqual(f.val, val)

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
    pass

class TestBytesField(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
