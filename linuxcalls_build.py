import cffi


def syscalls():
    with open("syscall_64.tbl", "r") as fh:
        for line in fh:
            line = line.rstrip()
            if len(line) == 0 or line.startswith("#"):
                continue

            nr, abi, name = line.split()[0:3]
            if abi not in ['common', '64']:
                continue

            yield nr, name


def wrapper(ret, name, args):
    stub = "{} sys_{}({})".format(ret, name, args)

    argnames = ["NR_" + name]
    if len(args) != 0:
        argnames.extend([arg.rsplit()[-1] for arg in args.split(',')])

    prelude = "" if ret == "void" else "return "

    impl = "{} {{ {}syscall({}); }}".format(stub, prelude, ", ".join(argnames))
    return stub + ";", impl


wrapper_specs = [
    ("ssize_t", "read", "int fd, void * buf, size_t count"),
    ("ssize_t", "write", "int fd, void * buf, size_t count"),
    ("int", "open", "const char * pathname, int flags, int mode"),
    ("int", "close", "int fd"),
    ("int", "stat", "const char * pathname, void * statbuf"),
    ("int", "fstat", "int fd, void * statbuf"),
    ("int", "lstat", "const char * pathname, void * statbuf"),
    ("int", "poll", "void * fds, int nfds, void * tmo_p, void * sigmask"),
    ("long", "lseek", "int fd, long offset, int whence"),
    ("void", "sync", ""),
    ("int", "syncfs", "int fd"),
    ("int", "gettid", ""),
    ("ssize_t", "readahead", "int fd, long offset, size_t count"),
    ("int", "reboot", "unsigned int magic, unsigned int magic2, int cmd, void * arg"),
    ("int", "fadvise64", "int fd, long offset, long len, int advice"),
]


def constants():
    with open("constants", "r") as fh:
        for line in fh:
            yield "#define {} ...".format(line.rstrip())


def c_lines():
    yield "extern long syscall(long number, ...);"
    for nr, name in syscalls():
        yield "#define NR_{} {}".format(name, nr)


stubs = []
impls = []
for w in wrapper_specs:
    stub, impl = wrapper(*w)
    stubs.append(stub)
    impls.append(impl)

impls.append("#include <fcntl.h>")
impls.append("#include <sys/mman.h>")
impls.append("#include <sys/statvfs.h>")
impls.append("#include <linux/reboot.h>")

for const in constants():
    stubs.append(const)

numbers = list(c_lines())
c_def = "\n".join(numbers + stubs)
c_source = "\n".join(numbers + impls)

print(c_def)

ffibuilder = cffi.FFI()
ffibuilder.set_source("linux_syscalls._syscalls", c_source)
ffibuilder.cdef(c_def)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
