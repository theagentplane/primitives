"""Smoke tests for the package scaffold."""

from importlib import resources

import agentplane_primitives


def test_version_is_exposed() -> None:
    assert agentplane_primitives.__version__
    assert isinstance(agentplane_primitives.__version__, str)


def test_package_is_typed() -> None:
    # PEP 561 marker: consumers (Chronicle, control plane, TokenOps) get our type hints.
    assert resources.files("agentplane_primitives").joinpath("py.typed").is_file()
