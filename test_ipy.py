import re
from pathlib import Path

import pytest

from ipy import get_dependencies

RE_EXAMPLE = re.compile(r"(#[^\n]+\n)*# *([\w ]*?) *\| *([\w ]*?) *\n(.+)", re.DOTALL)


def load_examples_stores_loads(filename):
    """
    load statement examples and their expected stores and loads from example files

    The example files contain test examples of statements with their
    stores (stored names) and loads (loaded names)

    They are divided in blocks, each separated by 2 blank lines
    Each block has a statement preceded by a comment in the form:
    # <stored variables> | <loaded variables>

    """
    source = Path(filename).read_text()
    groups = re.split("\n\n\n+", source)[1:]  # skip the header comment
    examples = [RE_EXAMPLE.match(s).groups() for s in groups]
    return [
        (stmt, stores.split(), loads.split()) for _, stores, loads, stmt in examples
    ]


@pytest.mark.parametrize(
    "statement, stores, loads", load_examples_stores_loads("tests/function_examples.py")
)
def test_get_dependencies(statement, stores, loads):
    assert get_dependencies(statement) == loads
