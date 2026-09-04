#Test functions in get_sandboxed_path.py
import unittest
from pathlib import Path
from functions.get_sandboxed_path import _get_sandboxed_BASE_path, _validate_permitted_dir, get_sandboxed_READ_path, get_sandboxed_WRITE_path

class testSandbox(unittest.TestCase):
    def test_base(self):
        self.assertIsInstance(_get_sandboxed_BASE_path(), Path)

    def test_read(self):
        self.assertIsInstance(get_sandboxed_READ_path(), Path)

    def test_write(self):
        self.assertIsInstance(get_sandboxed_WRITE_path(), Path)

if __name__ == "__main__":
    unittest.main()