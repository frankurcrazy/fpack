#!/usr/bin/env python

import unittest

try:
    from fpack import *
except ImportError:
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(".", "..")))
    from fpack import *


class TestMessage(unittest.TestCase):
    def test_message_declaration(self):
        class Hello(Message):
            Fields = [
                field_factory("MsgID", Uint8),
                field_factory("Greetings", String),
            ]

        hello = Hello(MsgID=123, Greetings="helloworld")

        self.assertEqual(hello.MsgID, 123)
        self.assertEqual(hello.Greetings, "helloworld")

    def test_message_pack(self):
        class Hello(Message):
            Fields = [
                field_factory("MsgID", Uint8),
                field_factory("Greetings", String),
            ]

        hello = Hello(MsgID=123, Greetings="helloworld")
        packed = hello.pack()
        golden = b"\x7b\x00\x0ahelloworld"

        self.assertEqual(packed, golden)

    def test_message_unpack(self):
        class Hello(Message):
            Fields = [
                field_factory("MsgID", Uint8),
                field_factory("Greetings", String),
            ]

        golden = b"\x7b\x00\x0ahelloworld"
        msg, len_ = Hello.from_bytes(golden)

        self.assertEqual(len(golden), len_)
        self.assertEqual(msg.MsgID, 123)
        self.assertEqual(msg.Greetings, "helloworld")

    def test_message_repr(self):
        class Hello(Message):
            Fields = [
                field_factory("MsgID", Uint8),
                field_factory("Greetings", String),
            ]

        hello = Hello(MsgID=123, Greetings="helloworld")
        self.assertEqual(str(hello), '<Hello MsgID=123 Greetings="helloworld">')

    def test_message_nonexist_key(self):
        class Hello(Message):
            Fields = [
                field_factory("MsgID", Uint8),
                field_factory("Greetings", String),
            ]

        hello = Hello(MsgID=123, Greetings="helloworld")

        self.assertEqual(hello.Name, None)

    def test_message_size(self):
        class Hello(Message):
            Fields = [
                field_factory("MsgID", Uint8),
                field_factory("Greetings", String),
            ]

        hello = Hello(MsgID=123, Greetings="helloworld")
        self.assertEqual(hello.size, 1 + 2 + 10)

    def test_nested_message(self):
        class Item(Message):
            Fields = [
                field_factory("Name", String),
                field_factory("Price", Uint32),
            ]

        class Catalog(Message):
            Fields = [
                field_factory("CatalogID", Uint8),
                field_factory("Item", Item),
            ]

        catalog = Catalog(CatalogID=1)
        catalog_item = catalog.Item
        catalog_item.Name = "Computer"
        catalog_item.Price = 100

        self.assertEqual(catalog.CatalogID, 1)
        self.assertEqual(catalog.Item.Name, "Computer")
        self.assertEqual(catalog.Item.Price, 100)
