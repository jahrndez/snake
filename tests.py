import unittest
import snake
import os

TEST_FILES_DIR = 'test_files/'

class TestBasic(unittest.TestCase):
    def setUp(self):
        out_files = ['basic']
        #clean
        root, dirs, files = next(os.walk(TEST_FILES_DIR))
        for filename in files:
            if filename[0] != "." and filename.endswith('.o'):
                os.remove(os.path.join(TEST_FILES_DIR, filename))
            if filename in out_files:
                os.remove(os.path.join(TEST_FILES_DIR, filename))

    def test_single_c_file(self):
        out_file = TEST_FILES_DIR + 'basic'
        target = snake.Target(out_file)
        target.depends_on(TEST_FILES_DIR + 'basic.c')
        self.assertTrue(os.path.isfile(out_file))

if __name__ == '__main__':
    unittest.main()
