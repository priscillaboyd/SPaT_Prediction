import os
import shutil
import unittest

from tools.Utils import root_path, output_fields, create_folder_if_not_exists, results_folder


class TestUtils(unittest.TestCase):

    def test_output_fields(self):
        output_fields_needed = ['Date', 'Time', 'Result', 'Phase']
        self.assertEqual(output_fields_needed, output_fields)

    def test_folder_is_created_if_not_exists(self):
        folder = root_path + "/temp/"
        # folder does not exist
        self.assertEqual(os.path.exists(folder), False)

        # folder created
        create_folder_if_not_exists(folder)
        self.assertEqual(os.path.exists(folder), True)

        # remove after test
        os.rmdir(folder)
        self.assertEqual(os.path.exists(folder), False)

    def test_results_folder_exists(self):
        create_folder_if_not_exists(results_folder)
        self.assertEqual(os.path.exists(results_folder), True)

        # remove folder after test
        shutil.rmtree(results_folder)
        self.assertEqual(os.path.exists(results_folder), False)


if __name__ == "__main__":
    unittest.main()
