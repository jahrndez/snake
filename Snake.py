class Dir:

    def __init__(self, dirname, recursive=False):
        """Constructs a directory target from the specified ‘dirname’. Every
        file in the directory is then treated as a dependency. The optional
        ‘recursive’ specifies whether any directories within this directory
        should also become part of the target; any operations
        (depends_on(), map(), build()) will be applied accordingly.
        """

    def __getitem__(self, name):
        """Returns the target with the specified name if this directory has it in its
        dependencies, throws an error otherwise.
        """

	def map(self, in, out):
        """Sets the output of this directory by creating a set of in->out relationships. ‘in’
        is a string with at most one wildcard, and specifies all files to which this rule
        will apply. ‘out’ is a string that specifies the output of all the input files
        matched by ‘in’. ‘out’ must have the same number of wildcards as ‘in’. Only
        dependencies of this directory which are matched by a call to map() will be built on
        build()
        """

	def depends_on(self, *dep):
        """Specifies the dependencies of this directory, i.e. its input in the dependency tree."""

	def tool(self, tool):
        """Specify the build tool for this Dir."""

	def has_tool(self):
        """Returns whether a build tool has been previously defined for this Dir."""

	def build(self, tool=None):
        """Build this directory with the specified tool. If no tool is specified here, a tool
    	must have been previously specified by a call to tool(). Only dependencies which are
    	bound to an output will be built.
        """

class Target:
    """Root of dependency tree."""

	def __init__(self, out=None):
        """Constructs a new target object, with an output optionally specified."""

	def map(self, out):
        """Sets this target’s output. This will be the final artifact after build() is
    	invoked on this target.
        """

	def depends_on(self, *dep):
        """Specify the dependencies of this target."""

	def tool(self, tool):
        """Specify the build tool for this target."""

	def has_tool(self):
        """Returns whether a build tool has been previously defined for this target."""

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

	def flags(self, *fl):
        """Options specified when running this tool. One flag per argument."""
