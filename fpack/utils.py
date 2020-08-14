#!/usr/bin/env python

""" utility functions used by fpack
"""

from io import BytesIO


def get_length(data):
    """ Get length of data

        Arguments:
            data: data to measure length
    """

    if isinstance(data, memoryview):
        return data.nbytes
    if isinstance(data, bytes):
        return len(data)
    if isinstance(data, str):
        return len(data)
    if isinstance(data, BytesIO):
        return data.getbuffer().nbytes
    if hasattr(data, "__iter__"):
        return len(data)
    if data is None:
        return 0

    raise ValueError(f"invalid type {type(data)}.")


__all__ = ["get_length"]
