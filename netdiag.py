import graphviz

"""Model a logical data flow diagram.

This module can build up an in-memory, logical representation of a
network of applications and their exchange of data. Can read in data
from a set of CSV files and output into the DOT language used by
Graphviz.
"""

system_fieldnames=["System",
                   "Environment",
                   "Descr",
                   "Functional Owner",
                   "Technical Owner",
                   "Sensitive",
                   "Cataloging",
                   "Inventory",
                   "Finance",
                   "User",
                   "Circ",
                   "License",
                   "Notes"
                   ]

def to_code(token: str):
    """Creates a lower-case 'code' from a string."""

    return token.lower().replace(' ','_').replace('.','_')

class Environment:
    """Represents an environment in which software systems are hosted."""

    def __init__(self, code: str, name: str, host: str, oncampus: bool):
        """Initializes an environment."""

        self.code = code
        self.name = name
        self.host = host
        self.oncampus = oncampus
        self.systems = []

    def add_system(self, system: object) -> None:
        """Adds a System to this Environment."""
        self.systems.append(system)

    def to_dot(self, indent=2) -> str:
        """Return a DOT string that describes this Enviroment."""

        pad = ' ' * indent
        subgraph = []
        subgraph.append(f'{pad}subgraph cluster_{self.code} {{')
        subgraph.append(f'{pad*2}label="{self.name}";')
        subgraph.append(f'{pad*2}labelloc="b";')
        subgraph.append(f'{pad*2}style=dashed;')
        if self.oncampus:
            subgraph.append(f'{pad*2}color="maroon";')
            subgraph.append(f'{pad*2}fontcolor="maroon";')
        subgraph.append('')
        for s in self.systems:
            subgraph.append(s.to_dot(indent = indent + 2))
        subgraph.append(f'{pad}}}')

        return '\n'.join(subgraph)

class System:
    """Represents a software system in this network.

    Atributes:
        code: A short name that will be used as an identifier within the
          network.
        name: The name used as the label of this system in a diagram
        environment: The name of the environment this system is hosted in,
          may be None.
    """

    def __init__(self, code: str, name: str, environment: str):
        """Initializes System object.

        Args:
            code: A short name that will be used as an identifier within the
              network.
            name: The name used as the label of this system in a diagram
            environment: The name of the environment this system is hosted in,
              may be None.

        """

        self.code = code
        self.name = name
        self.environment = environment

    def to_dot(self, indent=2) -> str:
        """Return a DOT string that describes this node."""

        # Note: before Python 3.12, f-string expression cannot contain
        # backslash character
        pad = ' ' * indent
        label = self.name.replace(' ','\\n')
        shape = "box"
        return f'{pad}{self.code} [label="{label}", shape={shape}];'

class DataFlow:
    """Represents the flow of data between two systems.

    Attributes:
      source: source system of the data.
      target: target systems, where the data lands.
      mode: read ('r') or write ('w'), i.e. does this merely read, or does it update data storage?
    """

    def __init__(self, source: str, target: str, mode: str):
        """Initializes this DataFlow."""

        self.source = source
        self.target = target
        self.mode = mode

    def to_dot(self, indent=2) -> str:
        """Returns a DOT string that creates an edgoe for this DataFlow."""

        pad = ' ' * indent
        s = to_code(self.source)
        t = to_code(self.target)
        style = 'dashed' if self.mode == 'r' else 'solid'

        return f'{pad}{s} -> {t} [style="{style}"]'

class Network:
    """This class represents a network with nodes, clusters, and edges."""

    def __init__(self, name: str):
        """Initializes this Environment.

        Attributes:
          name: Name used for this Network diagram.
          environments: hosting Environments represented in this Network.
          systems: Systems in this Network not otherwise in an Environment.
          dataflows: DataFlows in this Network.
        """

        self.name = name
        self.environments={}
        self.systems={}
        self.dataflows = []

    def add_dataflow(self, df) -> None:
        """Adds a DataFlow to this Network."""

        self.dataflows.append(df)

    def add_environment(self, environment: Environment) -> None:
        """Adds Environments to this Network."""

        self.environments[environment.code] = environment

    def add_system(self, system: System) -> None:
        """Adds Systems to this Network."""

        env_code = to_code(system.environment)
        if env_code in self.environments:
            self.environments[env_code].add_system(system)
        else:
            self.systems[system.code] = system

    def write_dot(self, out):
        """Writes a DOT-language diagram of this network.

        This version calls to_dot() methods on each object which
        return strings of Graphviz code that represent each object.

        Args:
          out: Writer object, like a file.

        """

        out.write(f'digraph {self.name} {{\n')
        for environment in self.environments.values():
            out.write(environment.to_dot())
            out.write('\n\n')
        for system in self.systems.values():
            out.write(system.to_dot())
            out.write('\n')
        out.write('\n\n')
        for df in self.dataflows:
            out.write(df.to_dot())
            out.write('\n')
        out.write('}\n')

    def graphviz(self, out):
        """Walk the Network and build up a graphviz object.
        """

        dot = graphviz.Digraph(self.name)
        for environment in self.environments.values():
            pass
