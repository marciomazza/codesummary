import ast
import builtins
from typing import List

ALL_BUILTINS = set(dir(builtins))


def get_dependencies(statement: str) -> List[str]:
    tree = ast.parse(statement)
    return [
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
        and isinstance(node.ctx, ast.Load)
        and node.id not in ALL_BUILTINS
    ]
