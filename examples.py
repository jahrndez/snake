from snake import Dir, Target, Tool

EXAMPLES_DIR = 'examples/'
FLAGS = '-W -Wall -I../.. -Wno-unused-function'
COMMAND = 'gcc {inp} -o {out} {flags} -lm'

target = Target(EXAMPLES_DIR + 'call_c_from_js/call_c_from_js')
target.depends_on(EXAMPLES_DIR + 'call_c_from_js/call_c_from_js.c')
target.depends_on(EXAMPLES_DIR + 'v7.c')
my_tool = Tool(COMMAND)
my_tool.flags(FLAGS)
target.tool(my_tool)
target.build()

target = Target(EXAMPLES_DIR + 'call_js_from_c/call_js_from_c')
target.depends_on(EXAMPLES_DIR + 'call_js_from_c/call_js_from_c.c')
target.depends_on(EXAMPLES_DIR + 'v7.c')
my_tool = Tool(COMMAND)
my_tool.flags(FLAGS)
target.tool(my_tool)
target.build()

target = Target(EXAMPLES_DIR + 'js_oop/js_oop')
target.depends_on(EXAMPLES_DIR + 'js_oop/js_oop.c')
target.depends_on(EXAMPLES_DIR + 'v7.c')
my_tool = Tool(COMMAND)
my_tool.flags(FLAGS)
target.tool(my_tool)
target.build()

target = Target(EXAMPLES_DIR + 'load_json_config/load_json_config')
target.depends_on(EXAMPLES_DIR + 'load_json_config/load_json_config.c')
target.depends_on(EXAMPLES_DIR + 'v7.c')
my_tool = Tool(COMMAND)

my_tool.flags(FLAGS)
target.tool(my_tool)
target.build()
