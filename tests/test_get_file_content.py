import unittest
from util import utils
from functions.get_file_content import get_file_content
from config import MAX_CHARS

class testFileContent(unittest.TestCase):
    # Ensure lorem file has content and that response is not an error (check for proper header)
    def test_lorem_file_length(self):
        #Get output of file read
        working_dir, file = "calculator", "lorem.txt"
        result = get_file_content(working_dir, file)
        # Check content and select the proper header
        result_header = utils.get_header(file, "FILE")
        header_length = len(result_header)
        content_length = len(result) - header_length
        # Assert
        self.assertTrue(content_length > 0 and result.startswith(result_header))

    # Ensure that lorem file is truncated (file exists to test truncation)
    def test_lorem_file_truncated(self):
        #Get output of file read
        working_dir, file = "calculator", "lorem.txt"
        result = get_file_content(working_dir, file)
        # Get truncation messages
        trunc_msg = utils.truncate_message(file, MAX_CHARS)
        result_end = result[-len(trunc_msg):]
        # Assert
        self.assertEqual(result_end, trunc_msg)

    # Ensure calculator file has content and that response is not an error
    def test_calculator_file(self):
        #Get output of file read
        working_dir, file = "calculator", "pkg/calculator.py"
        result = get_file_content(working_dir, file)
        # Check content and select the proper header
        result_header = utils.get_header(file, "FILE")
        header_length = len(result_header)
        content_length = len(result) - header_length
        # Assert
        self.assertTrue(content_length > 0 and result.startswith(result_header))

    def test_main_file(self):
        #Get output of file read
        working_dir, file = "calculator", "main.py"
        result = get_file_content(working_dir, file)
        # Check content and select the proper header
        result_header = utils.get_header(file, "FILE")
        header_length = len(result_header)
        content_length = len(result) - header_length
        # Assert
        self.assertTrue(content_length > 0 and result.startswith(result_header))

    def test_bin_file(self):
        # Get output of file read
        working_dir, file = "calculator", "/bin/cat"
        result = get_file_content(working_dir, file)
        # Assert error message
        expected_error_msg = utils.error_message_dir_not_auth(file)
        self.assertEqual(result, expected_error_msg)

    def test_not_exist_file(self):
        # Get output of file read
        working_dir, file = "calculator", "pkg/does_not_exist.py"
        result = get_file_content(working_dir, file)
        # Assert error message
        expected_error_msg_header = utils.error_message_generic_with_header(file, "")
        self.assertTrue(result.startswith(expected_error_msg_header))

#Functions for examining file content 
def content_length(file_content) -> int:
    return len(file_content)

def content_truncated(file_content) -> bool:
    return 'truncated' in file_content

if __name__ == "__main__":
    unittest.main(verbosity=2)