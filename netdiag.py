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
        return '{0}{1} [label="{2}", shape={shape}];\n'.format(pad, self.code, label, shape='box')

class Network:
    def __init__(self, name:str):
        self.name = name
        self.systems={}

    def add_sys(self, system:System):
        self.systems[system.code] = system

    def write_graphviz(self, out):
        out.write(f'graph {self.name} {{\n')
        for system in self.systems.values():
            # Note: before Python 3.12, f-string expression cannot contain backslash character
            out.write(system.to_graphviz())
        out.write('}\n')
