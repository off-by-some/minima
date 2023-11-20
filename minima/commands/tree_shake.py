import ast

from minima.visitors.code_extractor import extract_code, find_dependencies
from minima.visitors.import_extractor import flatten_imports

def tree_shake(file_paths):
    main_file = file_paths[0]

    with open(main_file, 'r') as file:
        main_content = file.read()
        main_tree = ast.parse(main_content)

    used_names = find_dependencies(main_tree)
    modified_contents = {}
    all_imports = set()

    # Iterate until no new dependencies are found
    previous_len = -1
    while previous_len != len(used_names):
        previous_len = len(used_names)
        for file_path in file_paths[1:]:
            modified_content, new_used_names, file_imports = extract_code(file_path, used_names, all_imports)
            used_names |= new_used_names
            all_imports |= file_imports
            modified_contents[file_path] = modified_content

    # Flatten and deduplicate imports
    flattened_imports = flatten_imports(all_imports)

    content = ""
    content += "".join(flattened_imports) + "\n"
    # Print the modified contents
    for file_path in file_paths[1:]:
        if file_path in modified_contents:
            content += '# file: ' + file_path + "\n"
            content += modified_contents[file_path]
            content += "\n\n"

    # Compact version of the main file
    compact_main_content = ast.unparse(main_tree)
    content += compact_main_content
    return content