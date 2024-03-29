import sys
import os
import subprocess
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist
from setuptools import setup, find_packages
import shutil

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))
PROTO_DIR = os.path.join(SETUP_DIR, "ra2yrproto")

PROTOC_EXE = os.environ.get("PROTOC_EXE", None) or shutil.which("protoc")

def get_proto_sources(p):
    for d, _, ff in os.walk(p):
        for f in ff:
            if f.endswith(".proto"):
                yield os.path.join(d, f)


class _Sdist(sdist):
    def run(self):
        sdist.run(self)


class BuildProto(build_py):
    def run(self):
        for p in get_proto_sources(PROTO_DIR):
            if (
                subprocess.call(
                    [
                        PROTOC_EXE,
                        "--python_out",
                        SETUP_DIR,
                        "--pyi_out",
                        SETUP_DIR,
                        "--proto_path",
                        SETUP_DIR,
                        p,
                    ]
                )
                != 0
            ):
                sys.exit(1)
        build_py.run(self)


setup(
    cmdclass={"sdist": _Sdist, "build_py": BuildProto},
    packages=find_packages(include=["ra2yrproto"]),
    package_data={"ra2yrproto": ["*.proto"]},
)
