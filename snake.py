import os
import re

ABS_PATH = os.path.realpath(__file__)

class Dir:
    def __init__(self, dirname, recursive=False):
        """Constructs a directory target from the specified ‘dirname’. Every
        file in the directory is then treated as a dependency. The optional
        ‘recursive’ specifies whether any directories within this directory
        should also become part of the target; any operations
        (depends_on(), map(), build()) will be applied accordingly.
        """

        # allow for full-paths to be used if they start with '/'
        if dirname[0] == "/":
            self.path = dirname
        else:
            self.path = os.path.join(ABS_PATH, dirname)
        if not os.path.isdir(self.path):
            raise Exception('specified directory does not exist')

        self.contents = [] # raw filename strings
        self.targets = {} # for files that became targets

        if recursive:
            for root, dirs, files in os.walk(self.path):
                for filename in files:
                    if filename[0] != '.':
                        self.contents.append(filename)
        else:
            root, dirs, files = next(os.walk(self.path))
            for filename in files:
                if filename[0] != ".":
                    self.contents(append(filename)

    def __getitem__(self, name):
        """Returns the target with the specified name if this directory has it in its
        dependencies, throws an error otherwise.
        """
        return self.targets[name]

    def map(self, input, out):
        """Sets the output of this directory by creating a set of in->out relationships. ‘in’
        is a string with at most one wildcard, and specifies all files to which this rule
        will apply. ‘out’ is a string that specifies the output of all the input files
        matched by ‘in’. ‘out’ must have the same number of wildcards as ‘in’. Only
        dependencies of this directory which are matched by a call to map() will be built on
        build()
        """
        if "*" in out and "*" not in input:
            raise Exception("In must have * if out has *")
        for f in self.contents:
            matches = re.search(input.replace("*", "(.)+"), f)
            if matches:
                self.targets[f] = Target(out.replace("*", matches.group(1)))

    def depends_on(self, *dep):
        """Specifies the dependencies of this directory, i.e. its input in the dependency tree."""

    def tool(self, tool):
        """Specify the build tool for this Dir."""
        self.tool = tool

    def has_tool(self):
        """Returns whether a build tool has been previously defined for this Dir."""
        return self.tool is not None

    def build(self, tool=None):
        """Build this directory with the specified tool. If no tool is specified here, a tool
        must have been previously specified by a call to tool(). Only dependencies which are
        bound to an output will be built.
        """

class Target:
    """Root of dependency tree."""

    def __init__(self, out=None):
        """Constructs a new target object, with an output optionally specified."""

    def out(self, out):
        """Sets this target’s output. This will be the final artifact after build() is
        invoked on this target.
        """

    def depends_on(self, *dep):
        """Specify the dependencies of this target."""

    def tool(self, tool):
        """Specify the build tool for this target."""
        self.tool = tool

    def has_tool(self):
        """Returns whether a build tool has been previously defined for this target."""
        return self.tool is None

    def build(self, tool=None):
        """Build this target with the specified tool. If no tool is specified here, a tool must
        have been specified previously by a call to tool(). This target’s output must have
        been previously set either in the constructor or in map().
        """

class Tool:

    def __init__(self, command):
        """The specified ‘command’ will be the actual program executed. The string
        must contain 2 mandatory placeholders ‘{in}’ and ‘{out}’ and may contain a third
        optional placeholder ‘{flags}’. At build-time, these will be replaced with the
        Target’s or Dir’s input and output, as well as with this tool’s flags. If the
        ‘{flags}’ placeholder is omitted, any flags will be appended to the end.
        """
        self.command = command

    def flags(self, *fl):
        """Options specified when running this tool. One flag per argument."""
        self.flags = fl

    def get_command(self):
        return command

    def get_flags(self):
        return flags
