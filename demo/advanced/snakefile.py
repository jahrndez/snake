
import snake
import sys

# Main GCC
gcc = snake.Tool("gcc {inp} -o {out}")
# Object gcc
obj_gcc = snake.Tool("gcc -c {inp} -o {out}")

# Util directory
util = snake.Dir('src/util')
util.tool(obj_gcc)
util.map('src/util/*.c', 'obj/util/*.o')

# Main exectuable
main_out = 'bin/main'
main_prog = snake.Target(main_out)
main_prog.depends_on('src/main.c', util)

# Test executable
test_out = 'bin/test'
test_prog = snake.Target(test_out)
test_prog.depends_on('src/test.c', util)

# Command line options
if len(sys.argv) == 1 or sys.argv[1] == 'main':
    gcc.flags("-v -O3")
    obj_gcc.flags("-v -O3")
    main_prog.build(gcc)
elif sys.argv[1] == 'test':
    gcc.flags("-v")
    obj_gcc.flags("-v")
    test_prog.build(gcc)
else:
    print("No such target '{}'".format(sys.argv[1]))
