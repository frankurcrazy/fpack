# fpack

[![PyPI version](https://badge.fury.io/py/fpack.svg?kill_cache=1)](https://badge.fury.io/py/fpack)
[![Build Status](https://travis-ci.com/frankurcrazy/fpack.svg?branch=master&kill_cached=1)](https://travis-ci.com/frankurcrazy/fpack)
[![Coverage Status](https://coveralls.io/repos/github/frankurcrazy/fpack/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/frankurcrazy/fpack?branch=master)

***fpack*** is a simple message (de)serializer created for fun and educational purpose.
fpack hasn't been widely deployed, so use it at your own risk.

## Requirements
 - python >= 3.7

## Installation
### Install with pip
```bash
pip install fpack
```

### Download latest version from git
```bash
git clone https://github.com/frankurcrazy/fpack
cd fpack && python setup.py install
```

## Guide
The following shows an example that uses fpack to declare and pack/unpack a message.

### Primitive types
***fpack*** supports primitive types:
 - Uint8
 - Uint16
 - Uint32
 - Uint64
 - Int8
 - Int16
 - Int32
 - Int64
 - Bytes
 - String

### Message declaration
```python
import fpack

# Declare a Hello message, with MsgID (`Uint8`) and Greeting (`String`) field.
class Hello(fpack.Message):
    Fields = [
        fpack.field_factory("MsgID", fpack.Uint8),
        fpack.field_factory("Greeting", fpack.String),
    ]
```

### Message serialization
```python
>>> helloMsg = Hello()
>>> helloMsg.MsgID = 100
>>> helloMsg.Greetings = "Helloworld!"
>>> helloMsg
<Hello MsgID=100 Greetings="Helloworld!">
>>> helloMsg.pack()
b'd\x00\x0bHelloworld!'
```

### Message deserialization
Message deserialization can be done by calling class method `from_bytes`, or by calling instance method `unpack`

Decode with class method `from_bytes`:
```python
>>> decodedMsg, decodedLength = Hello.from_bytes(b'd\x00\x0bHelloworld!')   # using the byte-stream from previous example
>>> decodedMsg
<Hello MsgID=100 Greetings=Helloworld!>
```

Decode with instance method `unpack`:
```python
>>> decodedMsg = Hello()
>>> decodedMsg.unpack(b'd\x00\x0bHelloworld!')
16
>>> decodedMsg
<Hello MsgID=100 Greetings="Helloworld!">
```

### Nested message (from 0.0.5 and beyond)
Nested message is supported.

Declaring an nested message:
```python
import fpack

class MailHeader(fpack.Message):
    Fields = [
        fpack.field_factory("Subject", fpack.String),
        fpack.field_factory("From", fpack.String),
        fpack.field_factory("To", fpack.String),
    ]

class MailBody(fpack.Message):
    Fields = [
        fpack.field_factory("Body", fpack.String),
        fpack.field_factory("Signature", fpack.String),
    ]

class Mail(fpack.Message):
    Fields = [
        fpack.field_factory("Header", MailHeader),
        fpack.field_factory("Body", MailBody),
    ]

>>> mail = Mail()
>>> header = mail.Header
>>> header.Subject = "this is a mail"
>>> header.From = "John Doe"
>>> header.To = "Jane Doe"
>>> body = mail.Body
>>> body.Text = "mail body"
>>> body.Signature = "by John doe"
>>> mail
<Mail Header=<Header Subject="this is a mail" From="John Doe" To="Jane Doe"> Body=<Body Text="mail body" Signature="by John doe">>
>>> mail.pack()
b'\x00\x0ethis is a mail\x00\x08John Doe\x00\x08Jane Doe\x00\tmail body\x00\x0bby John doe'
```

### Array (from 1.0.0 and beyond)
Array field is supported and can be created via ```array_field_factory(name, type)```.

```python
import fpack

class Item(fpack.Message):
    Fields = [
        fpack.field_factory("Name", fpack.String),
        fpack.field_factory("Price", fpack.Uint32),
    ]

class Catalog(fpack.Message):
    Fields = [
        fpack.field_factory("CatalogID", fpack.Uint8),
        fpack.array_field_factory("Items", Item),
    ]

items = [
    Item(Name="Camera", Price=10),
    Item(Name="Computer", Price=12),
    Item(Name="Dildo", Price=5),
]

>>> catalog = Catalog(CatalogID=1, Items=items)
<Catalog CatalogID=1 Items=<Items length=3 items=[<Item Name="Camera" Price=10>,<Item Name="Computer" Price=12>,<Item Name="Dildo" Price=5>]>>
>>> catalog.pack()
b'\x01\x00\x03\x00\x06Camera\x00\x00\x00\n\x00\x08Computer\x00\x00\x00\x0c\x00\x05Dildo\x00\x00\x00\x05'
```

## License
BSD
