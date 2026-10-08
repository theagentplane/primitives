"""Tests for the metadata helpers."""

from agentplane_primitives.utils import is_reserved_key


def test_reserved_prefix() -> None:
    assert is_reserved_key("chronicle.sdk_version")
    assert not is_reserved_key("chroniclex.a")
    assert not is_reserved_key("client.library")
