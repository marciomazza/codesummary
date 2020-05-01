import re
from pathlib import Path

import pytest

from ipy import get_stores_and_loads

ID = r"([\.\w ]*?)"
RE_EXAMPLE = re.compile(fr"(#[^\n]+\n)*# *{ID} *\| *{ID} *\n(.+)", re.DOTALL)


def load_examples_stores_loads():
    """
    load statement examples and their expected stores and loads from example files

    The example files contain test examples of statements with their
    stores (stored names) and loads (loaded names)

    They are divided in blocks, each separated by 2 blank lines
    Each block has a statement preceded by a comment in the form:
    # <stored variables> | <loaded variables>

    """
    for path in Path("test_examples/").glob("*.py"):
        for block in re.split(r"\n#*\n#*\n+", path.read_text()):
            _, stores, loads, stmt = RE_EXAMPLE.match(block).groups()
            stores, loads = [l.split() for l in (stores, loads)]
            yield (stmt, stores, loads)
            if stmt.startswith("def "):
                # reuse function examples as async
                stmt = stmt.replace("def ", "async def ")
                yield (stmt, stores, loads)


@pytest.mark.parametrize("statement, stores, loads", load_examples_stores_loads())
def test_get_dependencies(statement, stores, loads):
    assert get_stores_and_loads(statement) == (stores, loads)
