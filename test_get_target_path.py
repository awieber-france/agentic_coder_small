#Test functions in get_sandboxed_path.py
import unittest
import utils
from pathlib import Path
from functions.get_target_path import get_target_path_READ_secure, get_target_path_WRITE_secure

class testTargetDir(unittest.TestCase):
    #---READ PERMISSSIONS---
    #Valid path 1 (directory)
    def test_read_valid_1(self):
        working_directory = "calculator"
        directory = "."
        result = get_target_path_READ_secure(working_directory, directory)
        self.assertIsInstance(result, Path)

    #Valid path 2 (directory)
    def test_read_valid_2(self):
        working_directory = "calculator"
        directory = "pkg"
        result = get_target_path_READ_secure(working_directory, directory)
        self.assertIsInstance(result, Path)

    #Valid path 2 (file)
    def test_read_not_dir(self):
        working_directory = "calculator"
        directory = "main.py"
        result = get_target_path_READ_secure(working_directory, directory)
        self.assertIsInstance(result, Path)

    #Outside working dir 2
    def test_read_outside_work_dir(self):
        working_directory = "calculator"
        directory = "/bin"
        expected_error_msg = utils.error_message_dir_not_auth(directory)
        result = get_target_path_READ_secure(working_directory, directory)
        self.assertTrue(result == expected_error_msg)

    #Outside working dir 2
    def test_read_outside_work_dir2(self):
        working_directory = "calculator"
        directory = "../"
        expected_error_msg = utils.error_message_dir_not_auth(directory)
        result = get_target_path_READ_secure(working_directory, directory)
        self.assertTrue(result == expected_error_msg)

    #Banned symlink symbol
    def test_read_symlink(self):
        working_directory = "calculator"
        directory = "pkg -> /etc"
        expected_error_msg = utils.error_message_symlink_present(directory)
        result = get_target_path_READ_secure(working_directory, directory)
        self.assertTrue(result == expected_error_msg)

    #---WRITE PERMISSSIONS---
    #Valid path 1 (directory)
    def test_write_valid(self):
        working_directory = "calculator"
        directory = "main.py"
        result = get_target_path_WRITE_secure(working_directory, directory)
        self.assertIsInstance(result, Path)

    #Overwrite existing directory 1
    def test_overwrite_existing_1(self):
        working_directory = "calculator"
        directory = "pkg"
        expected_error_msg = utils.error_message_overwrite_dir(directory)
        result = get_target_path_WRITE_secure(working_directory, directory)
        self.assertTrue(result == expected_error_msg)

    #Overwrite existing directory 2
    def test_overwrite_existing_2(self):
        working_directory = "calculator"
        directory = "pkg"
        expected_error_msg = utils.error_message_overwrite_dir(directory)
        result = get_target_path_WRITE_secure(working_directory, directory)
        self.assertTrue(result == expected_error_msg)

    #Valid path 2 (file)
    def test_write_not_dir(self):
        working_directory = "calculator"
        directory = "main.py"
        result = get_target_path_WRITE_secure(working_directory, directory)
        self.assertIsInstance(result, Path)

    #Outside working dir 2
    def test_write_outside_work_dir(self):
        working_directory = "calculator"
        directory = "/bin"
        expected_error_msg = utils.error_message_dir_not_auth(directory)
        result = get_target_path_WRITE_secure(working_directory, directory)
        self.assertTrue(result == expected_error_msg)

    #Outside working dir 2
    def test_write_outside_work_dir2(self):
        working_directory = "calculator"
        directory = "../"
        expected_error_msg = utils.error_message_dir_not_auth(directory)
        result = get_target_path_WRITE_secure(working_directory, directory)
        self.assertTrue(result == expected_error_msg)

    #Banned symlink symbol
    def test_write_symlink(self):
        working_directory = "calculator"
        directory = "pkg -> /etc"
        expected_error_msg = utils.error_message_symlink_present(directory)
        result = get_target_path_WRITE_secure(working_directory, directory)
        self.assertTrue(result == expected_error_msg)

if __name__ == "__main__":
    unittest.main()