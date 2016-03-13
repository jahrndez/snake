import unittest
import snake
import os

TEST_FILES_DIR = 'test_files/'


class TestBasic(unittest.TestCase):
    def setUp(self):
        out_files = ['basic']
        # clean
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
        my_tool = snake.Tool("gcc {inp} -o {out}")
        target.tool(my_tool)
        target.build()
        self.assertTrue(os.path.isfile(out_file))

    def test_two_c_files(self):
        out_file = TEST_FILES_DIR + 'basic'
        target = snake.Target(out_file)
        target.depends_on(TEST_FILES_DIR + 'basic.c', TEST_FILES_DIR + 'basic2.c')
        my_tool = snake.Tool("gcc {inp} -o {out}")
        target.tool(my_tool)
        target.build()
        self.assertTrue(os.path.isfile(out_file))

    def test_basic_flags(self):
        out_file = TEST_FILES_DIR + 'basic'
        target = snake.Target(out_file)
        target.depends_on(TEST_FILES_DIR + 'basic.c')
        my_tool = snake.Tool("gcc {inp} {flags} {out}")
        my_tool.flags("-o")
        target.tool(my_tool)
        target.build()
        self.assertTrue(os.path.isfile(out_file))

    def test_single_folder_deps_single_folder(self):
        out_file = TEST_FILES_DIR + 'dir1/a.o'
        path = TEST_FILES_DIR + 'dir1'
        dir1 = snake.Dir(path,True)
        dir1.map('*.c','*.o')
        dir1.depends_on(TEST_FILES_DIR + 'basic.c')
        my_tool = snake.Tool("gcc {inp} -o {out}")
        dir1.tool(my_tool)
        dir1.build()
        self.assertTrue(os.path.isfile(TEST_FILES_DIR + 'dir1/a.o'))

    def test_flags_no_placeholder(self):
        out_file = TEST_FILES_DIR + 'basic'
        target = snake.Target(out_file)
        target.depends_on(TEST_FILES_DIR + 'basic.c')
        my_tool = snake.Tool("gcc {inp} -o {out}")
        my_tool.flags("-Wall")
        target.tool(my_tool)
        target.build()
        self.assertTrue(os.path.isfile(out_file))

if __name__ == '__main__':
    unittest.main()
