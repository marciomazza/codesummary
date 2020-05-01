import re
from pathlib import Path

import pytest

from ipy import get_stores_and_loads

ID = r"([\.\w ]*?)"
RE_EXAMPLE = re.compile(fr"(#[^\n]+\n)*# *{ID} *\| *{ID} *\n(.+)", re.DOTALL)
EXAMPLES_DIR = "test_examples"


def source_replace(filename, old, new):
    source = Path(filename).read_text()
    return source.replace(old, new)


def load_example_sources():
    for path in Path(EXAMPLES_DIR).glob("*.py"):
        yield path.read_text()
    # reuse function examples as coroutines
    yield source_replace(f"{EXAMPLES_DIR}/function_definition.py", "def ", "async def ")
    # reuse comprehension examples as async comprehensions
    yield source_replace(f"{EXAMPLES_DIR}/comprehensions.py", " for ", " async for ")


def load_examples_stores_loads():
    """
    load statement examples and their expected stores and loads from example files

    The example files contain test examples of statements with their
    stores (stored names) and loads (loaded names)

    They are divided in blocks, each separated by 2 blank lines
    Each block has a statement preceded by a comment in the form:
    # <stored variables> | <loaded variables>

    """
    for source in load_example_sources():
        for block in re.split(r"\n#*\n#*\n+", source):
            _, stores, loads, stmt = RE_EXAMPLE.match(block).groups()
            yield (stmt, stores.split(), loads.split())


@pytest.mark.parametrize("statement, stores, loads", load_examples_stores_loads())
def test_get_dependencies(statement, stores, loads):
    assert get_stores_and_loads(statement) == (stores, loads)
