import pytest
import os

pytest_plugins = "tmpdir"

def run(cmd, ignore_errors=False):
    retcode = os.system(cmd)
    if retcode != 0 and not ignore_errors:
        raise Exception("Command failed: %s" % cmd)

class TestConanGypGenerator(object):
    def test_basic(self):
        run("conan config install gyp-generator.py -tf generators")
        run("git clone https://github.com/czoido/conan-node-module && cd conan-node-module && "
            "mkdir conan_build && cd conan_build && "
            "npm install && "
            "conan install .. --build=missing && npm install")
