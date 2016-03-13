import unittest
import snake
import os

TEST_FILES_DIR = 'test_files/'


def clean():
    # clean
        bin_ = TEST_FILES_DIR + 'bin/'
        out_ = TEST_FILES_DIR + 'obj/'
        for root, _, files in os.walk(bin_):
            for filename in files:
                if filename[0] != '.':
                    os.remove(os.path.join(root, filename))

        for root, _, files in os.walk(out_):
            for filename in files:
                if filename[0] != '.':
                    os.remove(os.path.join(root, filename))


class TestBasic(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

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
        clean()

    def tearDown(self):
        clean()

    def test_single_dir(self):
        out_file = TEST_FILES_DIR + 'obj/dir1/a.o'
        path = TEST_FILES_DIR + 'src/dir1/'
        dir1 = snake.Dir(path)
        dir1.map(TEST_FILES_DIR + 'src/dir1/*.c', TEST_FILES_DIR + 'obj/dir1/*.o')
        my_tool = snake.Tool("gcc {inp} -o {out}")
        dir1.tool(my_tool)
        dir1.build()
        self.assertTrue(os.path.isfile(out_file))

    def test_single_dir_deps_single_file(self):

    def test_single_dir_deps_single_dir(self):

    def test_single_dir_deps_single_dir_and_file(self):

    def test_single_file_deps_single_dir_and_file(self):


class TestUseCases(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()

    def test_advanced(self):
        clang = snake.Tool("clang {in} -o {out}").flags("-v")
        op_clang = snake.Tool("clang {in} -o {out}").flags("-O3", "-v")
        util = snake.Dir('src/util')
        util.map(TEST_FILES_DIR + 'src/util/*.c', TEST_FILES_DIR + 'obj/util/*.o')

        main_out = TEST_FILES_DIR + 'bin/main'
        main_prog = snake.Target(main_out)
        main_prog.depends_on(TEST_FILES_DIR + 'src/basic.c')
        main_prog.depends_on(util)

        test_out = TEST_FILES_DIR + 'bin/test'
        test_prog = snake.Target(test_out)
        test_prog.depends_on(TEST_FILES_DIR + 'src/basic2.c')
        test_prog.depends_on(util)

        main_prog.build(op_clang)
        test_prog.build(clang)

        self.assertTrue(os.path.isfile(main_out))
        self.assertTrue(os.path.isfile(test_out))

if __name__ == '__main__':
    unittest.main()
