import unittest
import utils
from functions.write_file import write_file

class test_write_file(unittest.TestCase):
    def test_file_working_dir(self):
        working_dir, file_path = "calculator", "lorem_test.txt"
        content = "wait, this isn't lorem ipsum"
        result = write_file(working_dir, file_path, content)
        expected_msg = utils.success_message_WRITE(file_path, content)
        self.assertEqual(result, expected_msg)

    def test_file_subdir_message(self):
        working_dir, file_path = "calculator", "pkg/morelorem.txt"
        content = "lorem ipsum dolor sit amet"
        result = write_file(working_dir, file_path, content)
        expected_msg = utils.success_message_WRITE(file_path, content)
        self.assertEqual(result, expected_msg)

    def test_file_no_auth_message(self):
        working_dir, file_path = "calculator", "/tmp/temp.txt"
        content = "this should not be allowed"
        result = write_file(working_dir, file_path, content)
        expected_msg_header = utils.write_fail_message_to_append()
        self.assertEqual(result[-len(expected_msg_header):], expected_msg_header)

if __name__ == "__main__":
    unittest.main()