"""Types for config utils."""

from collections.abc import MutableMapping, Sequence
from datetime import date, datetime
from typing import Any, TypeGuard

# Type aliases for configuration values
ConfigScalar = str | int | float | datetime | date | None
ConfigSequence = Sequence[ConfigScalar]
# Recursive type definition using a forward reference.
ConfigMapping = MutableMapping[str, "ConfigMapping | ConfigScalar | ConfigSequence"]


def is_scalar(value: Any) -> TypeGuard[ConfigScalar]:
    """Check if the value is considered a configuration scalar.

    Args:
        value: Any value to check.

    Returns:
        True if value is a scalar, False otherwise.

    """
    return isinstance(value, (str, int, float, datetime, date)) or value is None


def is_sequence(value: Any) -> TypeGuard[ConfigSequence]:
    """Check if the value is considered a configuration sequence.

    Excludes strings even though they are sequences.

    Args:
        value: Any value to check.

    Returns:
        True if value is a list or tuple, False otherwise.

    """
    return isinstance(value, (list, tuple))


def is_mapping(value: Any) -> TypeGuard[ConfigMapping]:
    """Check if the value is considered a configuration mapping (dictionary).

    Args:
        value: Any value to check.

    Returns:
        True if value is a dictionary, False otherwise.

    """
    return isinstance(value, dict)
