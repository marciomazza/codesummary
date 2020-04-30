import ast
import builtins
from typing import List

BUILTINS = set(dir(builtins))


class DependencyTrackingVisitor(ast.NodeVisitor):
    @property
    def current_scope(self):
        return self.scopes[-1]

    def visit_FunctionDef(self, node):
        self.current_scope.append(node.name)  # store function name itself
        args = node.args
        argument_names = [
            a.arg
            for arglist in (
                args.posonlyargs,
                args.args,
                args.kwonlyargs,
                [a for a in (args.vararg, args.kwarg) if a],
            )
            for a in arglist
        ]
        self.scopes.append(argument_names)
        self.generic_visit(node)
        self.scopes.pop()  # restore outer scope

    def store(self, name, ctx):
        if isinstance(ctx, (ast.Store, ast.Del)):
            self.current_scope.append(name)
            return True
        else:
            return False

    def visit_Name(self, node):
        if self.store(node.id, node.ctx):
            ...  # done
        elif isinstance(node.ctx, ast.Load) and not any(
            node.id in seen for seen in (BUILTINS, *self.scopes, self.loads,)
        ):
            self.loads.append(node.id)

    def visit_Subscript(self, node):
        self.generic_visit(node)
        if isinstance(node.value, ast.Name):
            self.store(node.value.id, node.ctx)

    def scan(self, statement):
        self.scopes, self.loads = [[]], []
        tree = ast.parse(statement)
        self.visit(tree)
        assert len(self.scopes) == 1
        return self.current_scope, self.loads


def get_stores_and_loads(statement: str) -> List[str]:
    return DependencyTrackingVisitor().scan(statement)
