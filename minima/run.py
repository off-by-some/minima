#!/usr/bin/env python3

import argparse
import os
import sys
import logging
import black
from minima.commands.resolve import resolve_dependencies
from minima.commands.summarize import summarize
from minima.commands.tree_shake import tree_shake

# Setup logging
logger = logging.getLogger(__name__)
log_level = os.environ.get("DEBUG_LOG_LEVEL", "INFO").upper()
logger.setLevel(log_level)
handler = logging.StreamHandler()
handler.setLevel(log_level)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)



def main():
    parser = argparse.ArgumentParser(description="minima: A Python code analysis tool")
    parser.add_argument(
        "files", nargs="+", help="Paths to the Python files to analyze", type=str
    )
    parser.add_argument("--dependencies", help="List dependencies", action="store_true")
    parser.add_argument(
        "--tree-shake", help="Perform tree shaking", action="store_true"
    )
    parser.add_argument(
        "--hide-methods", help="Omit class methods", action="store_true"
    )
    parser.add_argument("--hide-functions", help="Omit functions", action="store_true")
    parser.add_argument(
        "--depth",
        help="Not implemented yet. Depth to resolve dependencies. a value of 2 looks at dependencies of the file, and it's dependencies",
        default=1,
    )
    parser.add_argument(
        "--show-return-values",
        help="Show return values, omit the function body",
        action="store_true",
    )
    args = parser.parse_args()

    all_content = ""
    all_file_paths = set()
    for python_file in args.files:
        if not os.path.exists(python_file):
            logger.error(f"🚨 The file {python_file} does not exist!")
            sys.exit(1)

        file_paths = list(resolve_dependencies(python_file))
        content = tree_shake(file_paths)

        all_file_paths |= set(file_paths)
        all_content += content + "\n\n"

    if args.dependencies:
        for file_path in set(all_file_paths):  # Use set to avoid duplicate paths
            print(file_path)
        return

    if args.tree_shake:
        print(content)
        return
        
    summarize(
        all_content, 
        hide_methods=args.hide_methods, 
        hide_functions=args.hide_functions,
        show_return_values=args.show_return_values
    )


if __name__ == "__main__":
    main()
