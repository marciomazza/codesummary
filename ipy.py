import ast
from contextlib import contextmanager
from functools import wraps
from typing import List, Tuple


def with_decorators_first(visit):
    @wraps(visit)
    def swap_decorator_list_and_body(self, node):
        fields = list(node._fields)
        i, j = [fields.index(f) for f in ("body", "decorator_list")]
        fields[i], fields[j] = fields[j], fields[i]
        node._fields = tuple(fields)
        return visit(self, node)

    return swap_decorator_list_and_body


def list_fields_except(node, field_name):
    return [field for name, field in ast.iter_fields(node) if name != field_name]


class DependencyTrackingVisitor(ast.NodeVisitor):
    @property
    def current_scope(self):
        return self.scopes[-1]

    def visit(self, node):
        # simplify to transparently visit lists
        if isinstance(node, list):
            for item in node:
                self.visit(item)
        elif isinstance(node, ast.AST):
            super().visit(node)

    def scan(self, statement):
        self.scopes, self.loads = [[]], []
        self.attributes = {}
        tree = ast.parse(statement)
        self.visit(tree)
        assert len(self.scopes) == 1
        return self.current_scope, self.loads

    def visit_Import(self, node):
        for name in node.names:
            self.store(name.asname or name.name)

    visit_ImportFrom = visit_Import

    def visit_Global(self, node):
        for name in node.names:
            self.loads.append(name)

    def store(self, name, ctx=ast.Store()):
        if isinstance(ctx, (ast.Store, ast.Del)):
            self.current_scope.append(name)
            return True
        else:
            return False

    def load(self, name):
        if not any(name in seen for seen in (*self.scopes, self.loads,)):
            self.loads.append(name)

    def store_or_load(self, name, ctx):
        self.store(name, ctx) or (isinstance(ctx, ast.Load) and self.load(name))

    def visit_Name(self, node):
        self.store_or_load(node.id, node.ctx)
        self.attributes[node] = node.id

    def visit_Attribute(self, node):
        self.generic_visit(node)
        base = self.attributes.get(node.value, None)
        if not base:
            return
        self.attributes[node] = name = f"{base}.{node.attr}"
        self.store_or_load(name, node.ctx)

    def visit_Subscript(self, node):
        self.generic_visit(node)
        if isinstance(node.value, ast.Name):
            self.store(node.value.id, node.ctx)

    def visit_Assign(self, node):
        # visit right side before left
        # so, when the same var appears on both sides, it is both loaded and stored
        self.visit(node.value)
        self.visit(node.targets)

    def visit_AugAssign(self, node):
        # visit the left side
        self.visit(node.target)
        # the left side is the last stored variable in the current scope
        # and is generally also a dependency of the augmented assignment
        #
        # to emulated that variable load before store, we:
        # remove it from the scope, try to load it and then store it back again
        var = self.current_scope.pop()
        self.load(var)
        self.store(var)
        # visit the right side
        self.visit(node.value)

    @contextmanager
    def new_scope(self, names=None):
        self.scopes.append(names or [])
        yield self.scopes[-1]  # current scope
        self.scopes.pop()

    def visit_ListComp(self, node):
        with self.new_scope():
            # first visit the generators ("for ... ") to store vars in the current scope
            self.visit(node.generators)
            # visit remaining fields
            self.visit(list_fields_except(node, "generators"))

    visit_SetComp = visit_ListComp
    visit_GeneratorExp = visit_ListComp
    visit_DictComp = visit_ListComp

    @with_decorators_first
    def visit_FunctionDef(self, node):
        self.store(node.name)  # store function name
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

    @with_decorators_first
    def visit_ClassDef(self, node):
        class_name = node.name
        self.store(class_name)
        with self.new_scope() as class_scope:
            self.generic_visit(node)
        self.current_scope.extend(f"{class_name}.{name}" for name in class_scope)


def get_stores_and_loads(statement: str) -> Tuple[List[str], List[str]]:
    return DependencyTrackingVisitor().scan(statement)


def build_dependency_tree(statements):
    current, deps = {}, {}
    for stmt in statements:
        stores, loads = get_stores_and_loads(stmt)
        node_deps = [current[v] for v in loads if v in current]
        if node_deps:
            deps[stmt] = node_deps
        for store in stores:
            current[store] = stmt
    return deps


def chain_dependencies(stmt, deps):
    if stmt in deps:
        for dep in deps[stmt]:
            yield from chain_dependencies(dep, deps)
    yield stmt


def summarize(statements):
    deps = build_dependency_tree(statements)
    last = statements[-1]
    return list(chain_dependencies(last, deps))
