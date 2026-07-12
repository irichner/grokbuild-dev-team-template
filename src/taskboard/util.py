"""Pure helpers used by the board and by Fixture B seeded-bug exercises."""


def clamp(n: float, lo: float, hi: float) -> float:
    """Clamp *n* into the inclusive range [*lo*, *hi*].

    Raises ValueError if lo > hi.
    """
    if lo > hi:
        raise ValueError(f"lo ({lo}) must be <= hi ({hi})")
    if n < lo:
        return lo
    if n > hi:
        return hi
    return n


def normalize_tag(s: str) -> str:
    """Normalize a tag: strip whitespace and lowercase.

    Raises ValueError if the result is empty (including whitespace-only input).
    """
    if not isinstance(s, str):
        raise TypeError(f"tag must be a str, got {type(s).__name__}")
    normalized = s.strip().lower()
    if not normalized:
        raise ValueError("tag must be a non-empty string")
    return normalized
