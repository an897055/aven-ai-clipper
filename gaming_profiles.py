"""Validated game-specific guidance for AVEN AI CLIPPER highlight selection.

Kept free of ML dependencies so request validation and prompt profiles can be
unit-tested without loading the video-processing stack.
"""
import os


SUPPORTED_GAMING_MODES = frozenset({"off", "pubg", "minecraft"})


def normalize_gaming_mode(value):
    """Return a supported gaming profile or raise ValueError."""
    mode = str(value or "off").strip().lower()
    if mode not in SUPPORTED_GAMING_MODES:
        raise ValueError("gaming_mode must be off, pubg, or minecraft")
    return mode


def apply_gaming_mode(env, value):
    """Set a validated per-job profile and clear any inherited profile.

    Mutates the supplied child-process environment and returns the normalized
    mode. This keeps general-video jobs isolated from stale server settings.
    """
    selected = normalize_gaming_mode(value)
    env.pop("AVEN_GAMING_MODE", None)
    if selected != "off":
        env["AVEN_GAMING_MODE"] = selected
    return selected


def gaming_guidance(mode=None):
    """Return grounded highlight-selection instructions for the selected game."""
    selected = normalize_gaming_mode(
        os.environ.get("AVEN_GAMING_MODE", "off") if mode is None else mode
    )
    if selected == "pubg":
        return """
GAMING PROFILE — PUBG / BGMI:
- Prefer genuine high-skill or high-stakes moments: clutch wins, squad wipes,
  1vX fights, clean headshots, sprays, sniper shots, close escapes, revives
  under pressure, final-circle decisions, rare/valuable loot, funny fails,
  unexpected bugs, and surprising tactical plays.
- Keep enough lead-in to understand the fight and enough aftermath to see the
  knock, elimination, win, or failure. Do not invent kills or outcomes.
- A loud gunfight alone is not automatically a highlight; prioritize clarity,
  skill, tension, surprise, and payoff.
"""
    if selected == "minecraft":
        return """
GAMING PROFILE — MINECRAFT:
- Prefer satisfying builds, clever redstone, rare discoveries, strong
  transformations, clutch survival, boss fights, speedrun moments, parkour,
  unexpected mobs, funny fails, near-death escapes, and surprising secrets.
- Keep the setup that makes a build, discovery, trick, or danger understandable,
  then include its payoff. Do not label ordinary mining or walking as a highlight.
- Do not invent items, achievements, or events that are not present.
"""
    return ""


def restore_gaming_mode(env, manifest):
    """Restore a persisted profile safely; legacy or malformed manifests use off."""
    raw = manifest.get("gaming_mode", "off") if isinstance(manifest, dict) else "off"
    try:
        return apply_gaming_mode(env, raw)
    except ValueError:
        return apply_gaming_mode(env, "off")
