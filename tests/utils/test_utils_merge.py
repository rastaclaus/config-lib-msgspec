"""Test cases for the merge module in config_lib.utils."""

from typing import TYPE_CHECKING

import pytest

from config_lib.utils.merge import _merge_values, update_recursive  # pyright: ignore[reportPrivateUsage]

if TYPE_CHECKING:
    from config_lib.utils.types import ConfigMapping

# Test cases for merge_values function


def test_merge_values_scalar() -> None:
    assert _merge_values(1, 2) == 2
    assert _merge_values("hello", "world") == "world"
    assert _merge_values(None, "value") == "value"
    assert _merge_values("value", None) == "value"
    assert _merge_values(None, None) is None


def test_merge_values_sequence() -> None:
    assert _merge_values([1, 2], [2, 3]) == [1, 2, 3]
    assert _merge_values((1, 2), (2, 3)) == [1, 2, 3]
    assert _merge_values([1, 2], None) == [1, 2]
    assert _merge_values(None, [1, 2]) == [1, 2]
    assert _merge_values((1, 2), None) == (1, 2)
    assert _merge_values(None, (1, 2)) == (1, 2)


def test_merge_values_mapping() -> None:
    assert _merge_values({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    assert _merge_values({"a": 1}, {"a": 2}) == {"a": 2}
    assert _merge_values({"a": {"b": 1}}, {"a": {"b": 2}}) == {"a": {"b": 2}}
    assert _merge_values({"a": {"b": 1}}, {"a": None}) == {"a": {"b": 1}}
    assert _merge_values({"a": None}, {"a": {"b": 2}}) == {"a": {"b": 2}}


def test_merge_values_incompatible_types() -> None:
    with pytest.raises(ValueError, match="Incompatible types for merging"):
        _merge_values([1, 2], {"a": 1})
    with pytest.raises(ValueError, match="Incompatible types for merging"):
        _merge_values({"a": 1}, [1, 2])


# Test cases for update_recursive function


def test_update_recursive_simple() -> None:
    target: ConfigMapping = {"a": 1, "b": 2}
    source: ConfigMapping = {"b": 3, "c": 4}
    assert update_recursive(target, source) == {"a": 1, "b": 3, "c": 4}


def test_update_recursive_nested() -> None:
    target: ConfigMapping = {"a": {"b": 1, "c": 2}}
    source: ConfigMapping = {"a": {"b": 3, "d": 4}}
    assert update_recursive(target, source) == {"a": {"b": 3, "c": 2, "d": 4}}


def test_update_recursive_sequences() -> None:
    target: ConfigMapping = {"a": [1, 2]}
    source: ConfigMapping = {"a": [2, 3]}
    assert update_recursive(target, source) == {"a": [1, 2, 3]}


def test_update_recursive_none_values() -> None:
    target: ConfigMapping = {"a": None, "b": 2}
    source: ConfigMapping = {"a": 1, "c": None}
    assert update_recursive(target, source) == {"a": 1, "b": 2, "c": None}


def test_update_recursive_incompatible_types() -> None:
    target: ConfigMapping = {"a": 1}
    source: ConfigMapping = {"a": [1, 2]}
    with pytest.raises(ValueError, match="Incompatible types for merging"):
        _ = update_recursive(target, source)


def test_update_recursive_non_dict() -> None:
    target = [1, 2]
    source = {"a": 1}
    with pytest.raises(TypeError):
        _ = update_recursive(target, source)  # pyright: ignore[reportArgumentType]

    target = {"a": 1}
    source = [1, 2]
    with pytest.raises(TypeError):
        _ = update_recursive(target, source)  # pyright: ignore[reportArgumentType]
