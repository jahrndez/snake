
import snake
import sys

# Regular gcc
clang = snake.Tool("gcc {inp} -o {out}")
clang.flags("-v")
# -O3 Optimized gcc
op_clang = snake.Tool("gcc {inp} -o {out}")
op_clang.flags("-O3", "-v")

# Util directory
util = snake.Dir('src/util')
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
    main_prog.build(op_clang)
elif sys.argv[1] == 'test':
    test_prog.build(clang)
else:
    print("No such target '{}'".format(sys.argv[1]))
