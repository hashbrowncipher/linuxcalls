import os

from linux_syscalls import errno
from linux_syscalls import NULL

from linux_syscalls import sync
from linux_syscalls import reboot

sync()
if reboot(0xfee1dead, 672274793, 0x1234567, NULL) != 0:
    e = errno()
    msg = os.strerror(e)
    raise OSError(e, msg)
