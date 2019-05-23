from ._syscalls import lib as _lib

from ctypes import Structure
from ctypes import c_char
from ctypes import c_long
from ctypes import c_ulong
from ctypes import c_uint

v = vars()
for field, value in _lib.__dict__.items():
    if field.upper() == field:
        v[field] = value

    if field.startswith('sys_'):
        v[field[4:]] = value

class Timespec(Structure):
    _fields_ = [
        ("tv_sec", c_ulong),
        ("tv_usec", c_ulong),
    ]

    def __repr__(self):
        return "Timespec({}.{})".format(self.tv_sec, self.tv_usec)


class Stat(Structure):
    _fields_ = [
        ("st_dev", c_ulong),
        ("st_ino", c_ulong),
        ("st_nlink", c_ulong),
        ("st_mode", c_uint),
        ("st_uid", c_uint),
        ("st_gid", c_uint),
        ("__pad0", c_char * 4),
        ("st_rdev", c_ulong),
        ("st_size", c_long),
        ("st_blksize", c_long),
        ("st_blkcnt", c_long),
        ("st_atim", Timespec), 
        ("st_mtim", Timespec),
        ("st_ctim", Timespec),
        ("__glibc_reserved", c_ulong * 3),
    ]

def errno():
    return _ffi.errno

NULL = _ffi.NULL
