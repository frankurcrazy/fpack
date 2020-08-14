"""fpack is a simple message (de)seriealizer in pure python
"""

from fpack.msg import *
from fpack.fields import *

__version__ = "0.0.6"
__author__ = "Frank Chang"
__author_email__ = "frank@csie.io"
__license__ = "BSD"
__all__ = [
    "Field", "Uint8", "Uint16", "Uint32", "Uint64", "Int8", "Int16",
    "Int32", "Int64", "Bytes", "String", "field_factory", "Message",
]
