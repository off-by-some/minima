import ast

from minima.visitors.dependency import DependencyFinder
from minima.visitors.import_extractor import extract_imports

def find_dependencies(node):
    finder = DependencyFinder()
    finder.visit(node)
    return finder.dependencies

class CodeExtractor(ast.NodeTransformer):
    def __init__(self, used_names, imports_to_exclude):
        self.used_names = used_names
        self.current_dependencies = set()
        self.imports_to_exclude = imports_to_exclude

    def visit_Import(self, node):
        for alias in node.names:
            if ("import", alias.name) in self.imports_to_exclude:
                return None
        return node

    def visit_ImportFrom(self, node):
        for alias in node.names:
            if ("from", node.module, alias.name) in self.imports_to_exclude:
                return None
        return node

    def visit_ClassDef(self, node):
        if node.name in self.used_names:
            self.current_dependencies |= find_dependencies(node)
            return node
        return None

    def visit_FunctionDef(self, node):
        if node.name in self.used_names:
            self.current_dependencies |= find_dependencies(node)
            return node
        return None

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in self.used_names:
                self.current_dependencies |= find_dependencies(node)
                return node
        return None


def extract_code(file_path, used_names, imports_to_exclude):
    with open(file_path, 'r') as file:
        content = file.read()
        tree = ast.parse(content)

    # Extract imports
    file_imports = extract_imports(tree)

    extractor = CodeExtractor(used_names, imports_to_exclude)
    new_tree = extractor.visit(tree)
    new_used_names = extractor.current_dependencies

    return ast.unparse(new_tree), new_used_names, file_imports