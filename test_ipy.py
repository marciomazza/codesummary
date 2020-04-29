import re
from pathlib import Path

import pytest

from ipy import get_dependencies

RE_STATEMENT = re.compile("( *# *([^\n]*)\n)+(.*)", re.DOTALL)


def load_statements_and_deps():
    """
    load statement examples and their expected dependencies from statement_stubs.py

    the last comment line in the beginning of each block lists the dependencies
    """
    source = Path("statement_stubs.py").read_text()
    statements = re.split("\n\n\n+", source)[1:]  # skip the header comment
    statements = [RE_STATEMENT.match(s).groups() for s in statements]
    return [(stmt, deps.split()) for _, deps, stmt in statements]


@pytest.mark.parametrize("statement, dependencies", load_statements_and_deps())
def test_get_dependencies(statement, dependencies):
    assert get_dependencies(statement) == dependencies
