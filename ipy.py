import ast
import builtins
from typing import List

BUILTINS = set(dir(builtins))


class DependencyTrackingVisitor(ast.NodeVisitor):

    # must be used only once to visit a tree,
    # grab the listed dependencies
    # and discard

    def __init__(self):
        self.scope = set()
        self.dependencies = []

    def visit_FunctionDef(self, node):
        argument_names = {a.arg for a in node.args.args}
        previous_scope = self.scope
        self.scope = self.scope | argument_names
        self.generic_visit(node)
        self.scope = previous_scope  # restore previous scope

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.scope.add(node.id)
        elif (
            isinstance(node.ctx, ast.Load)
            and node.id not in BUILTINS
            and node.id not in self.scope
            and node.id not in self.dependencies
        ):
            self.dependencies.append(node.id)


def get_dependencies(statement: str) -> List[str]:
    visitor = DependencyTrackingVisitor()
    tree = ast.parse(statement)
    visitor.visit(tree)
    return visitor.dependencies
