import pytest

from config_lib.sources import env


def test_get_env_values_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TEST_PREFIX_KEY", raising=False)
    assert env.get_env_values("TEST_PREFIX_") == {}


def test_get_env_values_single(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_PREFIX_KEY", "value")
    assert env.get_env_values("TEST_PREFIX_") == {"key": "value"}


def test_get_env_values_multiple(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_PREFIX_KEY1", "value1")
    monkeypatch.setenv("TEST_PREFIX_KEY2", "value2")
    result = env.get_env_values("TEST_PREFIX_")
    assert result == {"key1": "value1", "key2": "value2"}


def test_get_env_values_nested(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_PREFIX_SECTION__KEY1", "value1")
    monkeypatch.setenv("TEST_PREFIX_SECTION__KEY2", "value2")
    result = env.get_env_values("TEST_PREFIX_")
    assert result == {"section": {"key1": "value1", "key2": "value2"}}


def test_get_env_values_nested_multiple_sections(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_PREFIX_SECTION1__KEY1", "value1")
    monkeypatch.setenv("TEST_PREFIX_SECTION2__KEY2", "value2")
    result = env.get_env_values("TEST_PREFIX_")
    assert result == {"section1": {"key1": "value1"}, "section2": {"key2": "value2"}}


def test_get_env_values_nested_with_scalar_conflict(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_PREFIX_SECTION__KEY1", "value1")
    monkeypatch.setenv("TEST_PREFIX_SECTION", "value2")
    with pytest.raises(
        ValueError,
        match="Conflicting keys: 'section' attempts to overwrite nested dictionary with scalar value.",
    ):
        _ = env.get_env_values("TEST_PREFIX_")


def test_get_env_values_lowercase_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_PREFIX_SECTION__KeY1", "value1")
    result = env.get_env_values("TEST_PREFIX_")
    assert result == {"section": {"key1": "value1"}}


def test_get_env_values_strips_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_PREFIX_KEY", "value")
    result = env.get_env_values("TEST_PREFIX_")
    assert "TEST_PREFIX_" not in next(iter(result.keys()))


def test_prepare() -> None:
    assert env._prepare("TEST_PREFIX_KEY", "TEST_PREFIX_") == "key"  # pyright: ignore[reportPrivateUsage]
    assert env._prepare("TEST_PREFIX_SECTION__KEY", "TEST_PREFIX_") == "section__key"  # pyright: ignore[reportPrivateUsage]


def test_get_prefixed_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_PREFIX_KEY1", "value1")
    monkeypatch.setenv("OTHER_KEY", "value2")
    result = env._get_prefixed_values("TEST_PREFIX_")  # pyright: ignore[reportPrivateUsage]
    assert "OTHER_KEY" not in result
    assert result["key1"] == "value1"
