import pytest

from guiderail import config


def test_env_file_is_loaded_without_overriding_real_variables(tmp_path, monkeypatch):
    env = tmp_path / ".env"
    env.write_text(
        "# comment\n\nGUIDERAIL_T_ONE=abc\nexport GUIDERAIL_T_TWO='quoted value'\n"
        'GUIDERAIL_T_THREE="dq"\nGUIDERAIL_T_KEEP=from_file\nnot a pair\n', encoding="utf-8")
    for name in ("GUIDERAIL_T_ONE", "GUIDERAIL_T_TWO", "GUIDERAIL_T_THREE"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("GUIDERAIL_T_KEEP", "from_env")
    config.load_env_file(env)
    import os

    assert os.environ["GUIDERAIL_T_ONE"] == "abc"
    assert os.environ["GUIDERAIL_T_TWO"] == "quoted value"
    assert os.environ["GUIDERAIL_T_THREE"] == "dq"
    assert os.environ["GUIDERAIL_T_KEEP"] == "from_env"
    for name in ("GUIDERAIL_T_ONE", "GUIDERAIL_T_TWO", "GUIDERAIL_T_THREE"):
        monkeypatch.delenv(name)


def test_missing_env_file_is_ignored(tmp_path):
    config.load_env_file(tmp_path / "nope.env")


def test_threshold_defaults_and_validates(monkeypatch):
    monkeypatch.delenv("GUIDERAIL_THRESHOLD", raising=False)
    assert config.threshold() == 0.6
    monkeypatch.setenv("GUIDERAIL_THRESHOLD", "1.5")
    with pytest.raises(ValueError):
        config.threshold()


def test_generator_name_validates(monkeypatch):
    monkeypatch.setenv("GUIDERAIL_GENERATOR", "LLM")
    assert config.generator_name() == "llm"
    monkeypatch.setenv("GUIDERAIL_GENERATOR", "magic")
    with pytest.raises(ValueError):
        config.generator_name()
