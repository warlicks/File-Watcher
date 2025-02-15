import os
import shutil
import pytest
from typing import List, Union


def test_directory_factory(
    files_in_root: int, child_directories: Union[List[tuple], None] = None
) -> str:
    """Generates directories for use in tests

    We still need to be careful using this. The FileWatcher.on_create() picked up the
    creation of some of these files. As a result I needed

    Args:
        files_in_root (int): _description_
        child_directories (List[tupel): Each tuple in the list represents a sub-directory.
          The position in the list represents the depth in directory tree. Index zero is
          one layer from the test_directory_root. The tuple represents the number of
          folders at that level and files in each folder.

    Returns:
        str: name of the root dir
    """
    root_path = "./tests/rootdir"
    if os.path.exists(root_path):
        shutil.rmtree(root_path)
    os.mkdir(root_path)

    # Make files in root
    for i in range(files_in_root):
        fname = f"test_{i}.ext"
        os.system(f"touch {os.path.join(root_path, fname)}")
    if child_directories is not None:
        for index, level in enumerate(child_directories):
            for i in range(level[0]):
                dir_name = f"level_{index}{chr(i + 1 + 96)}"
                os.mkdir(os.path.join(root_path, dir_name))
                for j in range(level[1]):
                    fname = f"text_{j}.ext"
                    os.system(f"touch {os.path.join(root_path, dir_name, fname)}")
    return root_path


@pytest.fixture()
def single_level_dir():
    """Fixture to create a test directory of one level and 2 files at the root."""
    root = test_directory_factory(2)
    yield
    shutil.rmtree(root)


@pytest.fixture()
def single_sub_directory():
    root = test_directory_factory(1, [(1, 1)])
    yield
    shutil.rmtree(root)
