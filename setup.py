from setuptools import setup

setup(
    name="linuxcalls",
    version="0.1",
    packages=["linuxcalls"],
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["linuxcalls_build.py:ffibuilder"],
    install_requires=["cffi>=1.0.0"],
)
