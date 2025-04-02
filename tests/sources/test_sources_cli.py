import argparse

import msgspec
import pytest

from config_lib.sources.cli import _add_arguments, get_cli_values  # pyright: ignore[reportPrivateUsage]


def test_config_from_cli_basic() -> None:
    class Config(msgspec.Struct):
        name: str
        value: int

    # Simulate command-line arguments
    import sys

    sys.argv = ["test_program", "--name", "test_name", "--value", "10"]

    config = get_cli_values(Config)
    assert config == {"name": "test_name", "value": 10}


def test_config_from_cli_missing_arguments() -> None:
    class Config(msgspec.Struct):
        name: str
        value: int

    # Simulate command-line arguments with missing 'value'
    import sys

    sys.argv = ["test_program", "--name", "test_name"]

    assert get_cli_values(Config) == {"name": "test_name"}


def test_config_from_cli_bad_type_arguments() -> None:
    class Config(msgspec.Struct):
        value: int

    # Simulate command-line arguments with an invalid 'value' (string instead of int)
    import sys

    sys.argv = ["test_program", "--value", "abc"]

    with pytest.raises(ValueError):
        assert get_cli_values(Config) == {"value": "abc"}


def test_config_from_cli_nested_structures() -> None:
    class NestedConfig(msgspec.Struct):
        nested_value: int

    class Config(msgspec.Struct):
        name: str
        nested: NestedConfig

    # Simulate command-line arguments for nested configuration
    import sys

    sys.argv = ["test_program", "--name", "test_name", "--nested.nested_value", "20"]

    config = get_cli_values(Config)
    assert config == {"name": "test_name", "nested": {"nested_value": 20}}


def test__add_arguments() -> None:
    parser = argparse.ArgumentParser()

    class NestedConfig(msgspec.Struct):
        nested_value: int

    class Config(msgspec.Struct):
        name: str
        nested: NestedConfig

    _add_arguments(parser, Config)
    actions = parser._actions
    assert len(actions) == 3
    assert actions[0].dest == "help"
    assert actions[1].dest == "name"
    assert actions[2].dest == "nested.nested_value"
