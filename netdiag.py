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

    return token.lower().replace(' ','_')

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

    def to_graphviz(self, indent=2) -> str:
        """Return a string that describes this Enviroment to Graphviz."""

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
            subgraph.append(s.to_graphviz(indent = indent+2))
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

    def to_graphviz(self, indent=2) -> str:
        """Return a string that defines a node in Graphviz."""

        # Note: before Python 3.12, f-string expression cannot contain
        # backslash character
        pad = ' ' * indent
        label = self.name.replace(' ','\\n')
        shape = "box"
        return f'{pad}{self.code} [label="{label}", shape={shape}];'

class Network:
    def __init__(self, name:str):
        """Initializes this Environment.

        Attributes:
          name: Name used for this Network diagram.
          environments: hosting environments represented in this Network.
          systems: Systems in this network not otherwise in an Environment.
        """

        self.name = name
        self.environments={}
        self.systems={}

    def add_environment(self, environment: Environment) -> None:
        """Adds Environments to this Network."""
        self.environments[environment.code] = environment

    def add_system(self, system:System) -> None:
        """Adds Systems to this Network."""

        env_code=to_code(system.environment)
        if env_code in self.environments:
            self.environments[env_code].add_system(system)
        else:
            self.systems[system.code] = system

    def write_graphviz(self, out):
        """Writes a Graphviz diagram of this network.

        Args:
          out: Writer object, like a file.
        """

        out.write(f'graph {self.name} {{\n')
        for environment in self.environments.values():
            out.write(environment.to_graphviz())
            out.write('\n\n')
        out.write('\n\n')
        for system in self.systems.values():
            out.write(system.to_graphviz())
            out.write('\n')
        out.write('}\n')
