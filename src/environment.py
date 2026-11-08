class Environment:
    def __init__(self, enclosing = None):
        self.values = {}
        self.enclosing = enclosing

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values.update({name : value})
            return 
        if self.enclosing is not None:
            self.enclosing.asign(name, value)
            return
        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
    
    def define(self, name, value):
        self.values.update({name : value})