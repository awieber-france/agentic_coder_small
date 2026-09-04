import unittest
import re
import utils
from functions.get_files_info import get_files_info

class testAccessRights(unittest.TestCase):
    #Access allowed
    def test_main(self):
        working_dir, dir = "calculator", "."
        result = get_files_info(working_dir, dir)
        self.assertTrue(bool(re.fullmatch(msg_success_pattern(dir), result.strip()))) #Check full message for pattern match
    def test_subdir(self):
        working_dir, dir = "calculator", "pkg"
        result = get_files_info(working_dir, dir)
        self.assertTrue(bool(re.fullmatch(msg_success_pattern(dir), result.strip()))) #Check full message for pattern match
    #Access not allowed
    def test_other_proj_dir(self):
        working_dir, dir = "functions", "."
        result = get_files_info(working_dir, dir)
        expected_error_msg = utils.error_message_dir_not_auth(dir)
        self.assertEqual(result, expected_error_msg)
    def test_outside_dir(self):
        working_dir, dir = "calculator", "/bin"
        result = get_files_info(working_dir, dir)
        expected_error_msg = utils.error_message_dir_not_auth(dir)
        self.assertEqual(result, expected_error_msg)
    def test_path_traverse(self):
        working_dir, dir = "calculator", "../"
        result = get_files_info(working_dir, dir)
        expected_error_msg = utils.error_message_dir_not_auth(dir)
        self.assertEqual(result, expected_error_msg)
    def test_path_traverse2(self):
        working_dir, dir = "calculator", "/../../etc"
        result = get_files_info(working_dir, dir)
        expected_error_msg = utils.error_message_dir_not_auth(dir)
        self.assertEqual(result, expected_error_msg)
    #Not directory
    def test_file(self):
        working_dir, dir = "calculator", "main.py"
        result = get_files_info(working_dir, dir)
        expected_error_msg = utils.error_message_not_dir(dir)
        print(result)
        self.assertEqual(result, expected_error_msg)
    def test_symlink(self):
        working_dir, dir = "calculator", "pkg -> /etc"
        result = get_files_info(working_dir, dir)
        expected_error_msg = utils.error_message_symlink_present(dir)
        self.assertEqual(result, expected_error_msg)
    def test_symlink2(self):
        working_dir, dir = "calculator", "pkg -> etc"
        result = get_files_info(working_dir, dir)
        expected_error_msg = utils.error_message_symlink_present(dir)
        self.assertEqual(result, expected_error_msg)

def msg_success_pattern(directory):
    raw_header = utils.success_message_with_header_DIR(directory, content="")
    escaped_header = re.escape(raw_header)
    pattern = (
            f"{escaped_header}"  # Header line
            r"(?:\s*-\s+.+?:\s+file_size=\d+\s+bytes,\s+is_dir=(?:True|False)(?:\r?\n|$))+" # 1 or more list items
        )
    return pattern

if __name__ == "__main__":
    unittest.main(verbosity=2)


