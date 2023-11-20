import ast

class ImportExtractor(ast.NodeVisitor):
    def __init__(self):
        self.imports = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(("import", alias.name))

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.add(("from", node.module, alias.name))

def flatten_imports(all_imports):
    flattened_imports = set()
    for imp in all_imports:
        if imp[0] == "import":
            flattened_imports.add(f"import {imp[1]}")
        elif imp[0] == "from":
            flattened_imports.add(f"from {imp[1]} import {imp[2]}")
    return "\n".join(sorted(flattened_imports))

def extract_imports(tree):
    extractor = ImportExtractor()
    extractor.visit(tree)
    return extractor.imports