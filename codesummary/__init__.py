"""Top-level package for codesummary."""

__author__ = """Marcio Mazza"""
__email__ = "marciomazza@gmail.com"
__version__ = "0.1.0"

from .codesummary import get_stores_and_loads, summarize  # noqa: F401
from .ipython_extension import load_ipython_extension  # noqa: F401
