import unittest
import utils
from functions.run_python_file import run_python_file 

class test_run_python_file(unittest.TestCase):
    def test_valide_file_1(self):
        args = ["calculator", "main.py"]
        result = run_python_file(*args)
        self.assertTrue(result.startswith("STDOUT:"))

    def test_valide_file_extra_args(self):
        args = ["calculator", "main.py", ["3 + 5"]]
        result = run_python_file(*args)
        self.assertTrue(result.startswith("STDOUT:"))

    def test_valide_file_2(self):
        args = ["calculator", "tests.py"]
        result = run_python_file(*args)
        strings_present = ["Ran ", " tests in ", "OK"]
        self.assertTrue(all(x in result for x in strings_present))

    def test_outside_working_dir(self):
        args = ["calculator", "../main.py"]
        result = run_python_file(*args)
        expected_msg = utils.error_message_dir_not_auth(args[1])
        self.assertEqual(result, expected_msg)

    def test_inexesistant_file(self):
        args = ["calculator", "nonexistent.py"]
        result = run_python_file(*args)
        expected_msg = utils.error_message_execute_file_not_exist(args[1])
        self.assertEqual(result, expected_msg)

    def test_invalide_filetype(self):
        args = ["calculator", "lorem.txt"]
        result = run_python_file(*args)
        expected_msg = utils.error_message_execute_filetype_invalid(args[1])
        self.assertEqual(result, expected_msg)

    def test_dir_not_auth(self):
        args = [".", "main.py"]
        result = run_python_file(*args)
        expected_msg = utils.error_message_dir_not_auth(args[1])
        self.assertEqual(result, expected_msg)

arg_combos = [["calculator", "main.py"],
                ["calculator", "main.py", ["3 + 5"]],
                ["calculator", "tests.py"],
                ["calculator", "../main.py"],
                ["calculator", "nonexistent.py"],
                ["calculator", "lorem.txt"],
                [".", "main.py"]
                ]

if __name__ == "__main__":
    unittest.main(verbosity=2)