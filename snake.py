import os
import re
import subprocess

ABS_PATH = os.path.realpath(__file__)


class Dir:
    def __init__(self, dirname, recursive=False):
        """Constructs a directory target from the specified dirname. Every
        file in the directory is then treated as a dependency. The optional
        recursive specifies whether any directories within this directory
        should also become part of the target; any operations
        (depends_on(), map(), build()) will be applied accordingly.
        """

        # allow for full-paths to be used if they start with '/'
        self.recursive = recursive
        if dirname[0] == "/":
            self.path = dirname
        else:
            self.path = os.path.join(ABS_PATH, dirname)
        if not os.path.isdir(self.path):
            raise Exception('specified directory does not exist')

        self.maps = []
        self.dependencies = []
        # self.contents = [] # raw filename strings
        # self.targets = {} # for files that became targets

        # if recursive:
        #    for root, dirs, files in os.walk(self.path):
        #        for filename in files:
        #            if filename[0] != '.':
        #                self.contents.append(filename)
        # else:
        #    root, dirs, files = next(os.walk(self.path))
        #    for filename in files:
        #        if filename[0] != ".":
        #            self.contents.append(filename)

    def map(self, input, out):
        """Sets the output of this directory by creating a set of in->out
        relationships. in is a string with at most one wildcard, and specifies
        all files to which this rule will apply. out is a string that specifies
        the output of all the input files matched by in. out must have the same
        number of wildcards as in (0 or 1). Only dependencies of this directory
        which are matched by a call to map() will be built on build()
        """
        self.maps.append({"in": input, "out": out})
        # if "*" in out and "*" not in input:
        #    raise Exception("In must have * if out has *")
        # for f in self.contents:
        #    matches = re.search(input.replace("*", "(.)+"), f)
        #    if matches:
        #        self.targets[f] = Target(out.replace("*", matches.group(1)))

    def depends_on(self, *deps):
        """Specifies the dependencies of this directory, i.e. its input in the
        dependency tree.
        """
        for dep in deps:
            if isinstance(dep, Target) or isinstance(dep, Dir):
                self.dependencies.append(dep)
            elif isinstance(dep, str):
                if dep[0] == "/":
                    self.dependencies.append(dep)
                else:
                    self.dependencies.append(os.path.join(ABS_PATH, dep))
            else:
                raise Exception('dependency must be one of: Target, Dir, or string')

    def tool(self, tool):
        """Specify the build tool for this Dir."""
        self.tool = tool

    def has_tool(self):
        """Returns whether a build tool has been previously defined for this
        Dir.
        """
        return self.tool is not None

    def build(self, tool=None):
        """Build this directory with the specified tool. If no tool is specified
        here, a tool must have been previously specified by a call to tool().
        Only dependencies which are bound to an output will be built.
        """
        # TODO
        # contents = scan dir
        # contents[i] = Target if contents[i] matches, else Leaf
        # for each target in contents:
        #    for each d in deps:
        #        target.depends(d)
        # build c
        pass


class Leaf:
    """Wrapper class for files"""

    def __init__(self, filename):
        self.filename = filename

    def has_tool(self):
        return True

    def build(self):
        return self.filename


class Target:
    """Root of dependency tree."""

    def __init__(self, out=None):
        """Constructs a new target object, with an output optionally specified.
        """
        self.out = out
        self.dependencies = []
        self.tool = None

    def out(self, out):
        """Sets this target's output. This will be the final artifact after
        build() is invoked on this target.
        :param out: specifies the filename of the output
        """
        self.out = out

    def depends_on(self, *deps):
        """Specify the dependencies of this target."""
        for dep in deps:
            if isinstance(dep, Target) or isinstance(dep, Dir):
                self.dependencies.append(dep)
            elif isinstance(dep, str):
                if dep[0] == "/":
                    self.dependencies.append(Leaf(dep))
                else:
                    self.dependencies.append(Leaf(os.path.join(ABS_PATH, dep)))
            else:
                raise Exception('dependency must be one of: Target, Dir, or string')

    def tool(self, tool):
        """Specify the build tool for this target.
        :param tool: program with which to build this Target
        """
        self.tool = tool

    def has_tool(self):
        """Returns whether a build tool has been previously defined for this
        target.
        """
        return self.tool is not None

    def build(self, tool=None):
        """Build this target with the specified tool. If no tool is specified
        here, a tool must have been specified previously by a call to tool().
        This target's output must have been previously set either in the
        constructor or in map().
        :param tool: program with which to build this Target
        """
        if self.out is None:
            raise Exception('out was never specified')
        if tool is not None:
            self.tool = tool
        if self.tool is None:
            raise Exception('no tool specified for target')

        ins = [dep.build() if dep.has_tool() else dep.build(self.tool) for dep in self.dependencies]
        command = self.tool.command()
        in_string = " ".join(ins)

        if self.tool.flags is None:
            command = command.format(inp=in_string, out=self.out)
        elif command.contains("{flags}"):
            command = command.format(inp=in_string, out=self.out, flags=" ".join(self.tool.flags()))
        else:
            command = command.format(inp=in_string, out=self.out) + " " + " ".join(self.tool.flags())

        try:
            subprocess.check_call(command.split(" "))
        except subprocess.CalledProcessError:
            raise Exception('build failed')

        return self.out


class Tool:
    def __init__(self, command):
        """The specified 'command' will be the actual program executed. The
        string must contain 2 mandatory placeholders \{inp\} and \{out\} and may
        contain a third optional placeholder \{flags\}. At build-time, these
        will be replaced with the Target's or Dir's input and output, as well as
        with this tool's flags. If the \{flags\} placeholder is omitted, any
        flags will be appended to the end.
        """
        self.command = command.strip()
        self.flags = None

    def flags(self, *fl):
        """Options specified when running this tool. One flag per argument."""
        self.flags = fl

    def command(self):
        return self.command

    def flags(self):
        return self.flags
