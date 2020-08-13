#!/usr/bin/env python

from io import BytesIO

def get_length(data):
    if isinstance(data, memoryview):
        return data.nbytes
    elif isinstance(data, bytes):
        return len(data)
    elif isinstance(data, str):
        return len(data)
    elif isinstance(data, BytesIO):
        return data.getbuffer().nbytes
    elif data is None:
        return 0
    else:
        raise ValueError(f"invalid type {type(data)}.")


__all__ = ["get_length"]
