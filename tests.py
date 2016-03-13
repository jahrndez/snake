import unittest
import snake
import os

TEST_FILES_DIR = 'test_files/'

def make_dirs():
    if not os.path.exists(TEST_FILES_DIR + 'bin'):
        os.makedirs(TEST_FILES_DIR + 'bin')
    if not os.path.exists(TEST_FILES_DIR + 'bin/use_cases'):
        os.makedirs(TEST_FILES_DIR + 'bin/use_cases')
    if not os.path.exists(TEST_FILES_DIR + 'obj'):
        os.makedirs(TEST_FILES_DIR + 'obj')
    for root, _, _ in os.walk(TEST_FILES_DIR + 'src'):
        if '/src/' in root:
            obj_dir = root.replace('/src/', '/obj/')
            if not os.path.exists(obj_dir):
                os.makedirs(obj_dir)

def clean():
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
        my_tool = snake.Tool("gcc -c {inp} -o {out}")
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
        my_tool = snake.Tool("gcc -c {inp} {flags} {out}")
        my_tool.flags("-o")
        target.tool(my_tool)
        target.build()
        self.assertTrue(os.path.isfile(out_file))

    def test_flags_no_placeholder(self):
        out_file = TEST_FILES_DIR + 'bin/basic'
        target = snake.Target(out_file)
        target.depends_on(TEST_FILES_DIR + 'src/basic.c')
        my_tool = snake.Tool("gcc -c {inp} -o {out}")
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
        out_file = TEST_FILES_DIR + 'obj/dir1/c.o'
        path = TEST_FILES_DIR + 'src/dir1/'
        dir1 = snake.Dir(path)
        dir1.map(TEST_FILES_DIR + 'src/dir1/*.c', TEST_FILES_DIR + 'obj/dir1/*.o')
        my_tool = snake.Tool("gcc -c {inp} -o {out}")
        dir1.tool(my_tool)
        dir1.build()
        self.assertTrue(os.path.isfile(out_file))

    def test_single_dir_deps_single_file(self):
        pass

    def test_single_dir_deps_single_dir(self):
        pass

    def test_single_dir_deps_single_dir_and_file(self):
        pass

    def test_single_file_deps_single_dir_and_file(self):
        pass


class TestUseCases(unittest.TestCase):
    def setUp(self):
        clean()

    def tearDown(self):
        clean()


if __name__ == '__main__':
    make_dirs()
    unittest.main()
