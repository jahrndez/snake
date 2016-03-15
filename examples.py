from snake import Dir, Target, Tool

EXAMPLES_DIR = 'examples/'
FLAGS = '-W -Wall -I../.. -Wno-unused-function'

target = Target('call_c_from_js/call_c_from_js')
target.depends_on('call_c_from_js/call_c_from_js.c')
target.depends_on('v7.c')
my_tool = Tool("gcc {inp} -o {out} {flags} -lm")
my_tool.flags(FLAGS)
target.tool(my_tool)
target.build()

target = Target('call_js_from_c/call_js_from_c')
target.depends_on('call_js_from_c/call_js_from_c.c')
target.depends_on('v7.c')
my_tool = Tool("gcc {inp} -o {out} {flags} -lm")
my_tool.flags(FLAGS)
target.tool(my_tool)
target.build()

target = Target('js_oop/js_oop')
target.depends_on('js_oop/js_oop.c')
target.depends_on('v7.c')
my_tool = Tool("gcc {inp} -o {out} {flags} -lm")
my_tool.flags(FLAGS)
target.tool(my_tool)
target.build()

target = Target('load_json_config/load_json_config')
target.depends_on('load_json_config/load_json_config.c')
target.depends_on('v7.c')
my_tool = Tool("gcc {inp} -o {out} {flags} -lm")
my_tool.flags(FLAGS)
target.tool(my_tool)
target.build()
