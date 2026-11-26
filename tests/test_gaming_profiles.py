"""Unit tests for AVEN AI CLIPPER gaming profiles."""
import pytest

from gaming_profiles import (
    SUPPORTED_GAMING_MODES,
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
    if expected == "bgmi":
        with pytest.raises(ValueError, match="gaming_mode"):
            normalize_gaming_mode(raw)
    else:
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
