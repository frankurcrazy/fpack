#!/usr/bin/env python

import io
import unittest

try:
    from fpack.utils import get_length
except ImportError:
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(".", "..")))
    from fpack.utils import get_length


class TestGetLength(unittest.TestCase):
    def test_get_length_memoryview(self):
        mv = memoryview(b"awekf;jawlekfa")
        self.assertEqual(get_length(mv), mv.nbytes)

    def test_get_length_bytes(self):
        b = b"qwldkjo;aiealiewfu"
        self.assertEqual(get_length(b), len(b))

    def test_get_length_str(self):
        s = "this is frank speaking."
        self.assertEqual(get_length(s), len(s))

    def test_get_length_bytes_io(self):
        bio = io.BytesIO(b"wlfae;ksddas.fafjew")
        self.assertEqual(get_length(bio), bio.getbuffer().nbytes)

    def test_get_length_none_type(self):
        self.assertEqual(get_length(None), 0)

    def test_get_length_invalid_type(self):
        with self.assertRaises(ValueError):
            get_length(object())

    def test_get_length_list(self):
        self.assertEqual(get_length([]), 0)

    def test_get_length_tuple(self):
        self.assertEqual(get_length((1, 2, 3)), 3)

    def test_get_length_dict(self):
        self.assertEqual(get_length({"hello": "world"}), 1)


if __name__ == "__main__":
    unittest.main()
