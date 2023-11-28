"""Model a logical data flow diagram.

This module can build up an in-memory, logical representation of a
network of applications and their exchange of data. Can read in data
from a set of CSV files and output into the DOT language used by
Graphviz.

Currently most objects provide two methods for interacting with the graphviz library:

`add_to_graph()`: The object receives a Graph or Digraph object and adds itself to the graph.
`digraph()`: the object creates a Digraph object that represents it, and the caller adds the result to the graph.

These two options have a different feel.
Returning an object that the caller will dispose of has a more composable feel, but the other method produces much tigheter DOT code.

Will need to decide on one or the other.

Meanwhile, either seem preferable to the original approach of formatting the DOT string directly.
"""

import graphviz

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

    def digraph(self) -> graphviz.Digraph:
        """Return a Digraph that represents this Environment as a cluster."""

        cluster_attr = {
            'label': self.name,
            'labelloc': 'b',
            'style': 'dashed',
        }
        if self.oncampus:
            cluster_attr |= {'color': 'maroon','fontcolor': 'maroon'}

        c = graphviz.Digraph(name=f'cluster_{self.code}',
                             graph_attr=cluster_attr)
        for system in self.systems:
            s = system.digraph()
            c.subgraph(s)
        return c

    def add_to_graph(self, dot):
        """Adds this Environment as a cluster to the given Dot object, a Graph or Digraph.

        Arguments:
        dot: graphviz context manager, result of Graph.subgraph()
        """
        cluster_attr = {
            'label': self.name,
            'labelloc': 'b',
            'style': 'dashed',
        }
        if self.oncampus:
            cluster_attr |= {'color': 'maroon','fontcolor': 'maroon'}

        with dot.subgraph(name=f'cluster_{self.code}',
                          graph_attr=cluster_attr) as c:
            for s in self.systems:
                s.add_to_graph(c)


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

    def digraph(self) -> graphviz.Digraph:
        """Return a Digraph that represents this System as a cluster."""

        label = self.name.replace(' ','\\n')
        shape = "box"

        sg = graphviz.Digraph(f'sg_{self.code}')
        sg.node(self.code, label, shape=shape)
        return sg

    def add_to_graph(self, dot):
        """Adds this System to the given Dot object, a Graph or Digraph.

        Arguments:
        dot: Dot obect, a Graph or Digraph (or a context manager from Dot.subgraph())
        """

        label = self.name.replace(' ','\\n')
        shape = "box"
        dot.node(self.code, label, shape=shape)

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


    def add_to_graph(self, dot):
        """Adds this DataFlow as an edge to the Dot graph."""

        s = to_code(self.source)
        t = to_code(self.target)
        style = 'dashed' if self.mode == 'r' else 'solid'
        dot.edge(s, t, style=style)

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


    def digraph(self):
        """Walk the Network and build up a graphviz object.
        """

        dot = graphviz.Digraph(self.name)
        for environment in self.environments.values():
            e = environment.digraph()
            dot.subgraph(e)
        for system in self.systems.values():
            s = system.digraph()
            dot.subgraph(s)

        for df in self.dataflows:
            df.add_to_graph(dot)

        return dot

    def digraph2(self) -> graphviz.graphs.BaseGraph:
        """Walk the Network and build up a graphviz object."""

        dot = graphviz.Digraph(self.name)
        for e in self.environments.values():
            e.add_to_graph(dot)
        for system in self.systems.values():
            system.add_to_graph(dot)
        for df in self.dataflows:
            df.add_to_graph(dot)

        return dot
