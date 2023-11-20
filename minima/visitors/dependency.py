import ast

class DependencyFinder(ast.NodeVisitor):
    def __init__(self):
        self.dependencies = set()

    def visit_Name(self, node):
        self.dependencies.add(node.id)

    def visit_Attribute(self, node):
        self.generic_visit(node)
        self.dependencies.add(node.attr)