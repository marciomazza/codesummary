import builtins
import re
import string
from pathlib import Path

import pytest

from ipy import get_stores_and_loads

ID = r"([\.\w ]*?)"
RE_EXAMPLE = re.compile(fr"(#[^\n]*\n)*# *{ID} *\| *{ID} *\n(.+)", re.DOTALL)
EXAMPLES_DIR = "test_examples"


def source_replace(filename, old, new):
    source = Path(filename).read_text()
    return source.replace(old, new)


def load_example_sources():
    for path in Path(EXAMPLES_DIR).glob("*.py"):
        yield path.read_text()
    # reuse function examples as coroutines
    yield source_replace(f"{EXAMPLES_DIR}/functions.py", "def ", "async def ")
    # reuse comprehension examples as async comprehensions
    yield source_replace(f"{EXAMPLES_DIR}/comprehensions.py", " for ", " async for ")


RE_ONE_LETTER_NAME = re.compile(r"\b[a-zA-Z]\b")
LETTERS_TO_BUILTINS = dict(
    zip(
        string.ascii_letters, [b for b in dir(builtins) if b.isalpha() and b.islower()],
    )
)


def replace_names_with_builtins(source):
    return RE_ONE_LETTER_NAME.sub(
        lambda match: LETTERS_TO_BUILTINS[match.group()], source
    )


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
        blocks = re.split(r"\n#*\n#*\n+", source)
        # replace names by builtins in some examples
        # to test that they can be used as normal identifiers
        #
        # (* take some examples from the end just because they're more complex)
        blocks += [replace_names_with_builtins(b) for b in blocks[-3:]]

        for block in blocks:
            _, stores, loads, stmt = RE_EXAMPLE.match(block).groups()
            yield (stmt, stores.split(), loads.split())


@pytest.mark.parametrize("statement, stores, loads", load_examples_stores_loads())
def test_get_dependencies(statement, stores, loads):
    assert get_stores_and_loads(statement) == (stores, loads)
