import ast

class SummarizeVisitor(ast.NodeVisitor):
    """
        SummarizeVisitor is a visitor that summarizes a python file.

        It:
            - Retains the class and function definitions that are used.
            - Retains the imports that are used.
            - Retains the assignments that are used.
            - Retains the docstrings that are used.
            - Retains the return statements that are used.
    """
import ast

class SummarizeVisitor(ast.NodeVisitor):
    def __init__(self, hide_methods=False, hide_functions=False, hide_function_bodies=False, show_return_values=False):
        self.indent_level = 0
        self.result = []
        self.hide_methods = hide_methods
        self.hide_functions = hide_functions
        self.hide_function_bodies = hide_function_bodies
        self.show_return_values = show_return_values

    def add_newline(self, count=1):
        self.result.extend(["\n" * count])

    def visit_ClassDef(self, node):
        self.add_newline(1)
        indent = '    ' * self.indent_level
        bases = ', '.join(ast.unparse(base) for base in node.bases)
        self.result.append(f"{indent}class {node.name}({bases}):")
        self.indent_level += 1
        for item in node.body:
            if not (self.hide_methods and isinstance(item, ast.FunctionDef)):
                self.visit(item)
        self.indent_level -= 1
        self.add_newline(1)

    def visit_FunctionDef(self, node):
        if self.hide_functions:
            return
        indent = '    ' * self.indent_level
        args = ', '.join(arg.arg for arg in node.args.args)
        self.result.append(f"\n{indent}def {node.name}({args}):")
        if not self.hide_function_bodies:
            self.indent_level += 1
            for sub_item in node.body:
                if isinstance(sub_item, ast.Return) or not self.show_return_values:
                    self.result.append(f"\n{indent}    {ast.unparse(sub_item)}")
            self.indent_level -= 1
        self.add_newline(2)

    def visit_Assign(self, node):
        indent = '    ' * self.indent_level
        for target in node.targets:
            self.result.append(f"\n{indent}{target.id} = {ast.unparse(node.value)}")

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Str):
            indent = '    ' * self.indent_level
            self.add_newline(1)
            self.result.append(f"{indent}# {ast.unparse(node.value)}")
            self.add_newline(1)
        else:
            super().visit_Expr(node)

    def generic_visit(self, node):
        super().generic_visit(node)