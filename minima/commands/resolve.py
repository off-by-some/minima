import ast
import os
import logging

logger = logging.getLogger(__name__)

def find_root_module_path(file_path, module_name):
    current_path = os.path.dirname(os.path.abspath(file_path))
    module_parts = module_name.split('.')

    while current_path != '/':
        potential_root = os.path.join(current_path, *module_parts)
        if os.path.exists(potential_root) or os.path.exists(potential_root + '.py'):
            return current_path
        current_path = os.path.dirname(current_path)

    return None

def resolve_module_path(module_name, root_path):
    logger.debug(f"Resolving module {module_name}...")
    parts = module_name.split('.')
    potential_path = os.path.join(root_path, *parts)

    if os.path.exists(potential_path + '.py'):
        return potential_path + '.py'
    elif os.path.exists(potential_path) and os.path.isdir(potential_path):
        init_path = os.path.join(potential_path, '__init__.py')
        return init_path if os.path.exists(init_path) else None

    return None

def find_imports_in_file(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for name in node.names:
                module_name = name.name if isinstance(node, ast.Import) else node.module
                if module_name:
                    yield module_name

def resolve_dependencies(file_path):
    yield (os.path.abspath(file_path))

    imports = list(find_imports_in_file(file_path))
    if not imports:
        logger.debug("No imports found.")
        return

    for module_name in imports:
        root_path = find_root_module_path(file_path, module_name)
        if not root_path:
            logger.debug(f"Unable to determine the root module for {module_name}.")
            continue

        resolved_path = resolve_module_path(module_name, root_path)
        if resolved_path:
            yield resolved_path

