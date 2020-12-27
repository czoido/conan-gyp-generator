import os
import pytest
import shutil


@pytest.fixture(scope="session", autouse=True)
def tests_setup_and_teardown(tmp_path_factory):
    temp_env = {
        'CONAN_USER_HOME': str(tmp_path_factory.mktemp("conan_home")),
    }
    old_environ = dict(os.environ)
    os.environ.update(temp_env)
    old_folder = os.getcwd()
    run_folder = str(tmp_path_factory.mktemp("run_folder"))
    shutil.copy2("../gyp-generator.py", os.path.join(run_folder, "gyp-generator.py"))
    os.chdir(run_folder)

    yield
    os.chdir(old_folder)
    os.environ.clear()
    os.environ.update(old_environ)
