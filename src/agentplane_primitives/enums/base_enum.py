"""``BaseEnum``: the parent of every closed enum in this package.

Members are strings, and ``str()`` and f-strings give the value (``"llm"``), not the member name
(``"Kind.LLM"``), on every supported Python version. ``enum.StrEnum`` would do this but needs
Python 3.11; this package supports 3.10.
"""

from enum import Enum


class BaseEnum(str, Enum):
    """A string enum whose text form is its value."""

    def __str__(self) -> str:
        return str(self.value)
