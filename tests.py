import unittest
import snake
import os

TEST_FILES_DIR = 'test_files/'


def remove_files(prefix, files):
    for filename in files:
        if filename[0] != '.':
            os.remove(os.path.join(prefix, filename))


class TestBasic(unittest.TestCase):
    def setUp(self):
        # clean
        bin_ = TEST_FILES_DIR + 'bin/'
        out_ = TEST_FILES_DIR + 'out/'
        for root, _, files in os.walk(bin_):
            for filename in files:
                if filename[0] != '.':
                    try:
                        os.remove(os.path.join(root, filename))
                    except:
                        pass

        for root, _, files in os.walk(out_):
            for filename in files:
                if filename[0] != '.':
                    try:
                        os.remove(os.path.join(root, filename))
                    except:
                        pass

    def test_single_c_file(self):
        out_file = TEST_FILES_DIR + 'bin/basic'
        target = snake.Target(out_file)
        target.depends_on(TEST_FILES_DIR + 'src/basic.c')
        my_tool = snake.Tool("gcc {inp} -o {out}")
        target.tool(my_tool)
        target.build()
        self.assertTrue(os.path.isfile(out_file))

    def test_two_c_files(self):
        out_file = TEST_FILES_DIR + 'bin/basic'
        target = snake.Target(out_file)
        target.depends_on(TEST_FILES_DIR + 'src/basic.c', TEST_FILES_DIR + 'src/basic2.c')
        my_tool = snake.Tool("gcc {inp} -o {out}")
        target.tool(my_tool)
        target.build()
        self.assertTrue(os.path.isfile(out_file))

    def test_basic_flags(self):
        out_file = TEST_FILES_DIR + 'bin/basic'
        target = snake.Target(out_file)
        target.depends_on(TEST_FILES_DIR + 'src/basic.c')
        my_tool = snake.Tool("gcc {inp} {flags} {out}")
        my_tool.flags("-o")
        target.tool(my_tool)
        target.build()
        self.assertTrue(os.path.isfile(out_file))

    def test_flags_no_placeholder(self):
        out_file = TEST_FILES_DIR + 'bin/basic'
        target = snake.Target(out_file)
        target.depends_on(TEST_FILES_DIR + 'src/basic.c')
        my_tool = snake.Tool("gcc {inp} -o {out}")
        my_tool.flags("-Wall")
        target.tool(my_tool)
        target.build()
        self.assertTrue(os.path.isfile(out_file))


class TestDirs(unittest.TestCase):
    def setUp(self):
        # clean
        bin_ = TEST_FILES_DIR + 'bin/'
        out_ = TEST_FILES_DIR + 'out/'
        for root, _, files in os.walk(bin_):
            for filename in files:
                if filename[0] != '.':
                    os.remove(os.path.join(root, filename))

        for root, _, files in os.walk(out_):
            for filename in files:
                if filename[0] != '.':
                    os.remove(os.path.join(root, filename))

    def test_single_dir(self):
        out_file = TEST_FILES_DIR + 'out/dir1/a.o'
        path = TEST_FILES_DIR + 'src/dir1'
        dir1 = snake.Dir(path)
        dir1.map(TEST_FILES_DIR + 'src/dir1/*.c', TEST_FILES_DIR + 'out/dir1/*.o')
        my_tool = snake.Tool("gcc {inp} -o {out}")
        dir1.tool(my_tool)
        dir1.build()
        self.assertTrue(os.path.isfile(out_file))

if __name__ == '__main__':
    unittest.main()
