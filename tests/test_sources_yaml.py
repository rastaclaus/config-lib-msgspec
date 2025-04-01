from pathlib import Path

import pytest

from config_lib.sources.yaml import get_yaml_values


@pytest.fixture
def valid_yaml_file(tmp_path: Path):
    d = tmp_path / "valid.yaml"
    _ = d.write_text("""
key1: value1
key2:
    subkey1: subvalue1
    subkey2: subvalue2
""")
    return d


@pytest.fixture
def invalid_yaml_file(tmp_path: Path):
    d = tmp_path / "invalid.yaml"
    _ = d.write_text("key1: value1\nkey2: value2\ninvalid_key: value3\ninvalid_key")
    return d


@pytest.fixture
def non_mapping_yaml_file(tmp_path: Path):
    d = tmp_path / "non_mapping.yaml"
    _ = d.write_text("- value1\n- value2\n- [1, 2, 3]")
    return d


def test_valid_yaml_file(valid_yaml_file: Path) -> None:
    result = get_yaml_values(str(valid_yaml_file))
    expected = {"key1": "value1", "key2": {"subkey1": "subvalue1", "subkey2": "subvalue2"}}
    assert result == expected


def test_non_existent_file() -> None:
    with pytest.raises(FileNotFoundError):
        _ = get_yaml_values("non_existent_file.yaml")


def test_invalid_yaml_file(invalid_yaml_file: Path) -> None:
    with pytest.raises(ValueError, match="An error occurred while parsing the YAML file"):
        _ = get_yaml_values(str(invalid_yaml_file))


def test_non_mapping_yaml_file(non_mapping_yaml_file: Path) -> None:
    with pytest.raises(ValueError, match="The parsed data is not a ConfigMapping, but list."):
        _ = get_yaml_values(str(non_mapping_yaml_file))


def test_none_file_path() -> None:
    result = get_yaml_values(None)
    assert result == {}
