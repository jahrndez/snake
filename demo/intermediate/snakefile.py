from snake import Dir, Target, Tool

target = Target('example/a.o')
target.depends_on('example/a.c')
target.depends_on('example/b.c')
my_tool = Tool("gcc {inp} {flags} -o {out}")
my_tool.flags('-O3 -std=c11')
target.tool(my_tool)
target.build()
