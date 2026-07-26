import ast
import sys
import json
from pathlib import Path

from ..models import Usage, Detection
from .module_name_finder import get_module_name

def get_files_as_ast(repo_root: str) -> dict:
    root_path = Path(repo_root).resolve()

    ast_dict = {}
    for file_path in root_path.rglob("*.py"):
        relative_path = str(file_path.relative_to(root_path))
        try:
            code = file_path.read_text(encoding="utf-8")
            ast_tree = ast.parse(code)
            ast_dict[relative_path] = (ast_tree, code.splitlines())
        except (SyntaxError, UnicodeDecodeError):
            continue

    return ast_dict

def find_audited_dep(ast_dict:dict, detections:list[Detection]) -> dict[str, list[Usage]]:
    module_to_package = {get_module_name(detection.package): detection.package for detection in detections}
    imports = {detection.package: [] for detection in detections}


    for relative_path, (ast_tree, source_lines) in ast_dict.items():
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    dep = alias.name.split('.')[0]
                    if dep in module_to_package:
                        imports[module_to_package[dep]].append(Usage(file=relative_path, line=node.lineno, code=source_lines[node.lineno - 1]))

            elif isinstance(node, ast.ImportFrom):
                if node.module is None:
                    continue
                dep = node.module.split('.')[0]
                if dep in module_to_package:
                    imports[module_to_package[dep]].append(Usage(file=relative_path, line=node.lineno, code=source_lines[node.lineno - 1]))
            else:
                continue


    return imports
    