"""Tests for config_lib/utils/nest.py."""

import pytest

from config_lib.utils.nest import nest_dict


def test_nest_dict_empty() -> None:
    """Test with an empty dictionary."""
    assert nest_dict({}) == {}


def test_nest_dict_flat() -> None:
    """Test with a flat dictionary (no nesting)."""
    source: dict[str, str] = {"a": "1", "b": "2"}
    assert nest_dict(source) == source


def test_nest_dict_simple_nesting() -> None:
    """Test with simple one-level nesting."""
    source: dict[str, str] = {"a__b": "1"}
    expected = {"a": {"b": "1"}}
    assert nest_dict(source) == expected


def test_nest_dict_multi_level_nesting() -> None:
    """Test with multi-level nesting."""
    source = {"a__b__c": "1"}
    expected = {"a": {"b": {"c": "1"}}}
    assert nest_dict(source) == expected


def test_nest_dict_mixed_nesting() -> None:
    """Test with a mix of nested and flat keys."""
    source = {"a__b": "1", "c": "2"}
    expected = {"a": {"b": "1"}, "c": "2"}
    assert nest_dict(source) == expected


def test_nest_dict_complex_nesting() -> None:
    """Test with a more complex nesting structure."""
    source: dict[str, str] = {"a__b__c": "1", "a__d": "2", "e": "3"}
    expected = {"a": {"b": {"c": "1"}, "d": "2"}, "e": "3"}
    assert nest_dict(source) == expected


def test_nest_dict_overwrite() -> None:
    """Test that nested keys overwrite existing keys."""
    source: dict[str, str] = {"a": "1", "a__b": "2"}
    with pytest.raises(ValueError, match="Conflicting keys: 'a' conflicts with a non-nested key"):
        _ = nest_dict(source)


def test_nest_dict_empty_key_part() -> None:
    """Test with an empty key part in the middle."""
    source: dict[str, str] = {"a____b": "1"}
    expected = {"a__": {"b": "1"}}
    assert nest_dict(source) == expected


def test_nest_dict_only_delimiter() -> None:
    """Test with a key that is only the delimiter."""
    source: dict[str, str] = {"__": "1"}
    with pytest.raises(ValueError, match="Key cannot be only the delimiter: '__'"):
        _ = nest_dict(source)


def test_nest_dict_custom_delimiter() -> None:
    """Test with a custom delimiter."""
    source: dict[str, str] = {"a||b": "1"}
    expected = {"a": {"b": "1"}}
    assert nest_dict(source, delimiter="||") == expected


def test_nest_dict_no_conflict_with_prefix() -> None:
    """Test that a flat key does not conflict with a nested key prefix."""
    source: dict[str, str] = {"a": "1", "s_d": "1"}
    assert nest_dict(source) == source


def test_nest_dict_key_start_with_delimiter() -> None:
    """Test that a key starting with the delimiter is handled correctly."""
    source: dict[str, str] = {"__s": "1"}
    assert nest_dict(source) == source


def test_nest_dict_delimiter_in_key() -> None:
    """Test that a key containing the delimiter as part of the key name is handled correctly."""
    source: dict[str, str] = {"s_d": "1"}
    assert nest_dict(source) == source


def test_nest_dict_conflict_nested_with_flat() -> None:
    """Test that a nested key conflicts with a flat key."""
    source: dict[str, str] = {"a__b": "1", "a": "1"}
    with pytest.raises(
        ValueError,
        match="Conflicting keys: 'a' attempts to overwrite nested dictionary with scalar value.",
    ):
        _ = nest_dict(source)


def test_nest_dict_conflict_nested_with_flat_prefix() -> None:
    """Test that a flat key conflicts with a nested key prefix."""
    source: dict[str, str] = {"a": "1", "a__b": "2"}
    with pytest.raises(ValueError, match="Conflicting keys: 'a' conflicts with a non-nested key"):
        _ = nest_dict(source)


def test_nest_dict_no_key() -> None:
    """Test with an empty key."""
    source: dict[str, str] = {"": "1"}
    assert nest_dict(source) == {}


def test_nest_dict_trailing_delimiter() -> None:
    """Test with a trailing delimiter in the key."""
    source: dict[str, str] = {"a__": "1"}
    expected: dict[str,  str] = {"a__": "1"}
    assert nest_dict(source) == expected


def test_nest_dict_multiple_delimiters() -> None:
    """Test with multiple consecutive delimiters."""
    source: dict[str, str] = {"a____b": "1"}
    expected = {"a__": {"b": "1"}}
    assert nest_dict(source) == expected


def test_nest_dict_skip_empty_key() -> None:
    """Test that empty keys are skipped."""
    source: dict[str, str] = {"": "1", "a": "2"}
    expected: dict[str, str] = {"a": "2"}
    assert nest_dict(source) == expected


def test_nest_dict_empty_string_value() -> None:
    """Test with an empty string as value."""
    source: dict[str, str] = {"a__b": ""}
    expected = {"a": {"b": ""}}

    assert nest_dict(source) == expected


def test_nest_dict_nested_key_conflict_with_existing_dict() -> None:
    """Test that attempting to overwrite an existing nested dictionary raises a ValueError."""
    source: dict[str, str] = {"a__b__c": "existing", "a__b": "new"}
    with pytest.raises(
        ValueError,
        match="Conflicting keys: 'a__b' conflicts with existing nested dictionary.",
    ):
        _ = nest_dict(source)


def test_nest_dict_nested_key_prefix_conflict() -> None:
    """Test conflict detection between nested key prefixes."""
    source: dict[str, str] = {"a__b": "1", "a__b__c": "2"}
    with pytest.raises(
        ValueError,
        match="Conflicting keys: 'a__b' conflicts with a non-nested key",
    ):
        _ = nest_dict(source)


def test_nest_dict_nested_key_with_multiple_empty_parts() -> None:
    """Test handling of keys with multiple consecutive empty parts."""
    source: dict[str, str] = {"a____b____c": "1"}
    expected = {"a__": {"b__": {"c": "1"}}}
    assert nest_dict(source) == expected
