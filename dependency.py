class Dependency:
    def __init__(self, group, name, version):
        self.group = group
        self.name = name
        self.version = version
    
    def toString(self):
        return f"'compile group: '{self.group}', name: '{self.name}', version: '{self.version}'"
