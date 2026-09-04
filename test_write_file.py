import unittest
import utils
from functions.write_file import write_file

class test_write_file(unittest.TestCase):
    #File in working directory (authorized)
    def test_file_py_format_working_dir(self):
        working_dir, file_path = "calculator", "lorem_test.py"
        content = "wait, this isn't lorem ipsum"
        result = write_file(working_dir, file_path, content)
        expected_msg = utils.error_message_create_filetype_invalid(file_path)
        self.assertEqual(result, expected_msg)

    #File in subdirectory (authorized)
    def test_file__py_format_subdir(self):
        working_dir, file_path = "calculator", "pkg/morelorem.py"
        content = "lorem ipsum dolor sit amet"
        result = write_file(working_dir, file_path, content)
        expected_msg = utils.error_message_create_filetype_invalid(file_path)
        self.assertEqual(result, expected_msg)

    #File in working directory (authorized)
    def test_file_txt_format_working_dir(self):
        working_dir, file_path = "calculator", "lorem_test.txt"
        content = "wait, this isn't lorem ipsum"
        result = write_file(working_dir, file_path, content)
        expected_msg = utils.success_message_WRITE(file_path, content)
        self.assertEqual(result, expected_msg)

    #File in subdirectory (authorized)
    def test_file_txt_format_subdir_message(self):
        working_dir, file_path = "calculator", "pkg/morelorem.txt"
        content = "lorem ipsum dolor sit amet"
        result = write_file(working_dir, file_path, content)
        expected_msg = utils.success_message_WRITE(file_path, content)
        self.assertEqual(result, expected_msg)

    #File in unauthorized directory
    def test_file_no_auth_message(self):
        working_dir, file_path = "calculator", "/tmp/temp.txt"
        content = "this should not be allowed"
        result = write_file(working_dir, file_path, content)
        expected_msg = utils.error_message_dir_not_auth(file_path)
        self.assertEqual(result, expected_msg)

    #Invalid filetype for new file
    def test_create_invalid_filetype(self):
        working_directory, file_path = "calculator", "majestic_composter.py"
        content = "I eat you for lunch."
        expected_error_msg = utils.error_message_create_filetype_invalid(file_path)
        result = write_file(working_directory, file_path, content)
        self.assertTrue(result == expected_error_msg)

    #Invalid filetype for overwrite
    def test_overwrite_invalid_filetype(self):
        working_directory, file_path = "calculator", "lorem_test_file.rtf"
        content = "lorem ipsum overwritten by test"
        expected_error_msg = utils.error_message_write_filetype_invalid(file_path)
        result = write_file(working_directory, file_path, content)
        self.assertTrue(result == expected_error_msg)

if __name__ == "__main__":
    unittest.main()