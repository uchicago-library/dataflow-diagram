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
    def __init__(self, code, name, environment):
        self.code = code
        self.name = name
        self.environment = environment
        
class Network:
    def __init__(self, name:str):
        self.name = name
        self.systems={}

    def add_sys(self, system:System):
        self.systems[system.code] = system

    def write_graphviz(self, out):
        out.write(f'graph {self.name} {{\n')
        for system, val in self.systems.items():
            # Note: before Python 3.12, f-string expression cannot contain backslash character
            out.write(f'  {system} [label="{val.name}", shape=box]')
            out.write('\n')
        out.write('}\n')
        

    
