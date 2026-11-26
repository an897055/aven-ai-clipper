"""Unit tests for AVEN AI CLIPPER gaming profiles."""
import pytest

from gaming_profiles import (
    SUPPORTED_GAMING_MODES,
    apply_gaming_mode,
    gaming_guidance,
    normalize_gaming_mode,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (None, "off"),
        ("", "off"),
        ("  PUBG ", "pubg"),
        ("Minecraft", "minecraft"),
        ("OFF", "off"),
    ],
)
def test_normalize_gaming_mode(raw, expected):
    assert normalize_gaming_mode(raw) == expected


@pytest.mark.parametrize("mode", ["", "BGMI", "valorant", "pubg-mobile", "minecraft-java", "true", 1])
def test_rejects_unknown_gaming_modes(mode):
    with pytest.raises(ValueError, match="gaming_mode"):
        normalize_gaming_mode(mode)


def test_supported_modes_are_explicit():
    assert SUPPORTED_GAMING_MODES == {"off", "pubg", "minecraft"}


def test_general_mode_adds_no_game_specific_guidance(monkeypatch):
    monkeypatch.delenv("AVEN_GAMING_MODE", raising=False)
    assert gaming_guidance() == ""
    assert gaming_guidance("off") == ""


def test_pubg_profile_prioritizes_real_gameplay_payoffs():
    prompt = gaming_guidance("pubg")
    assert "PUBG / BGMI" in prompt
    assert "squad wipes" in prompt
    assert "Do not invent kills or outcomes" in prompt
    assert "A loud gunfight alone is not automatically a highlight" in prompt


def test_minecraft_profile_prioritizes_gameplay_discoveries():
    prompt = gaming_guidance("minecraft")
    assert "MINECRAFT" in prompt
    assert "redstone" in prompt
    assert "boss fights" in prompt
    assert "Do not invent items, achievements, or events" in prompt


def test_environment_profile_is_normalized(monkeypatch):
    monkeypatch.setenv("AVEN_GAMING_MODE", "  MINECRAFT ")
    assert "GAMING PROFILE — MINECRAFT" in gaming_guidance()


@pytest.mark.parametrize("mode", ["off", "pubg", "minecraft"])
def test_apply_gaming_mode_sets_exact_child_profile(mode):
    env = {"PATH": "/usr/bin", "AVEN_GAMING_MODE": "stale"}
    assert apply_gaming_mode(env, mode) == mode
    if mode == "off":
        assert "AVEN_GAMING_MODE" not in env
    else:
        assert env["AVEN_GAMING_MODE"] == mode
    assert env["PATH"] == "/usr/bin"


def test_apply_gaming_mode_rejects_invalid_value_without_mutating_env():
    env = {"AVEN_GAMING_MODE": "existing"}
    with pytest.raises(ValueError, match="gaming_mode"):
        apply_gaming_mode(env, "unknown")
    assert env == {"AVEN_GAMING_MODE": "existing"}
