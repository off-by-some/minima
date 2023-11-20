import ast
from minima.visitors.summarize import SummarizeVisitor
from rich.console import Console
from rich.syntax import Syntax
import re

def summarize(content, hide_methods=False, hide_functions=False, show_return_values=False):
    tree = ast.parse(content)

    visitor = SummarizeVisitor(
        hide_functions=hide_functions, 
        hide_methods=hide_methods, 
        show_return_values=show_return_values
    )
    visitor.visit(tree)

    formatted_code = ''.join(visitor.result).strip()

    # Replace more than two consecutive newlines with two newlines
    formatted_code = re.sub(r'\n{3,}', '\n\n', formatted_code)

    console = Console()
    syntax = Syntax(formatted_code, "python", theme="monokai", word_wrap=True)
    console.print(syntax)
