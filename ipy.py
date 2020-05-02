import ast
import builtins
from contextlib import contextmanager
from typing import List, Tuple

BUILTINS = set(dir(builtins))


class DependencyTrackingVisitor(ast.NodeVisitor):
    @property
    def current_scope(self):
        return self.scopes[-1]

    def scan(self, statement):
        self.scopes, self.loads = [[]], []
        self.attributes = {}
        tree = ast.parse(statement)
        self.visit(tree)
        assert len(self.scopes) == 1
        return self.current_scope, self.loads

    def visit_Import(self, node):
        for name in node.names:
            self.current_scope.append(name.asname or name.name)

    visit_ImportFrom = visit_Import

    def visit_Global(self, node):
        for name in node.names:
            self.loads.append(name)

    def store(self, name, ctx):
        if isinstance(ctx, (ast.Store, ast.Del)):
            self.current_scope.append(name)
            return True
        else:
            return False

    def store_or_load(self, name, ctx):
        if self.store(name, ctx):
            ...  # done
        elif isinstance(ctx, ast.Load) and not any(
            name in seen for seen in (BUILTINS, *self.scopes, self.loads,)
        ):
            self.loads.append(name)

    def visit_Name(self, node):
        self.store_or_load(node.id, node.ctx)

    def visit_Attribute(self, node):
        self.generic_visit(node)
        if isinstance(node.value, ast.Name):
            base = node.value.id
        elif isinstance(node.value, ast.Attribute):
            base = self.attributes[node.value]
        self.attributes[node] = name = f"{base}.{node.attr}"
        self.store_or_load(name, node.ctx)

    def visit_Subscript(self, node):
        self.generic_visit(node)
        if isinstance(node.value, ast.Name):
            self.store(node.value.id, node.ctx)

    @contextmanager
    def new_scope(self, names=None):
        self.scopes.append(names or [])
        yield self.scopes[-1]  # current scope
        self.scopes.pop()

    def visit_ListComp(self, node):
        with self.new_scope():
            # first visit the generators ("for ... ") to store vars in the current scope
            for gen in node.generators:
                self.visit(gen)
            # visit remaining fields
            for name, field in ast.iter_fields(node):
                if name != "generators":
                    self.visit(field)

    visit_SetComp = visit_ListComp
    visit_GeneratorExp = visit_ListComp
    visit_DictComp = visit_ListComp

    def visit_FunctionDef(self, node):
        self.current_scope.append(node.name)  # store function name
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
        with self.new_scope(argument_names):
            self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef


def get_stores_and_loads(statement: str) -> Tuple[List[str], List[str]]:
    return DependencyTrackingVisitor().scan(statement)
