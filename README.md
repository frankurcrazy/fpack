# fpack

[![PyPI version](https://badge.fury.io/py/fpack.svg?kill_cache=1)](https://badge.fury.io/py/fpack)
[![Build Status](https://travis-ci.com/frankurcrazy/fpack.svg?branch=master&kill_cached=1)](https://travis-ci.com/frankurcrazy/fpack)
[![Coverage Status](https://coveralls.io/repos/github/frankurcrazy/fpack/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/frankurcrazy/fpack?branch=master)

***fpack*** is a simple message (de)serializer created for fun and educational purpose.
fpack hasn't been widely deployed, and neither has it been fully tested. So use it at your own risk.

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

## License
BSD
