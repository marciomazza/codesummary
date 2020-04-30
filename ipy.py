import ast
import builtins
from typing import List

BUILTINS = set(dir(builtins))


class DependencyTrackingVisitor(ast.NodeVisitor):

    # must be used only once to visit a tree,
    # grab the listed dependencies
    # and discard

    def __init__(self):
        self.scopes = [set()]
        self.dependencies = []

    @property
    def current_scope(self):
        return self.scopes[-1]

    def visit_FunctionDef(self, node):
        self.current_scope.add(node.name)  # store function name itself
        argument_names = {a.arg for a in node.args.args}
        self.scopes.append(argument_names)
        self.generic_visit(node)
        self.scopes.pop()  # restore outer scope

    def visit_Name(self, node):
        # there is no case to consider the ast.Del context:
        # after a "del var" an outer "var" declaration does not become visible
        # neither in the current nor in inner scopes
        if isinstance(node.ctx, ast.Store):
            self.current_scope.add(node.id)
        elif (
            isinstance(node.ctx, ast.Load)
            and node.id not in BUILTINS
            and node.id not in set.union(*self.scopes)
            and node.id not in self.dependencies
        ):
            self.dependencies.append(node.id)


def get_dependencies(statement: str) -> List[str]:
    visitor = DependencyTrackingVisitor()
    tree = ast.parse(statement)
    visitor.visit(tree)
    return visitor.dependencies
