from __future__ import annotations

from typing import Iterable, List

from app.core.config import get_settings
from app.rag.filters import check_prompt_injection


def deny_by_default_user_prompt(question: str, *, max_chars: int) -> None:
    if len(question) > max_chars:
        raise ValueError("prompt_too_large")

    res = check_prompt_injection(question)
    if not res.ok:
        raise ValueError(f"prompt_injection:{res.reason}")


def allowlisted_source(source: str) -> bool:
    settings = get_settings()
    allow = settings.allowlist_sources_list
    if not allow:
        return True
    return source.strip() in allow


def filter_retrieved_chunks(chunks: Iterable[tuple[str, str]]) -> List[tuple[str, str]]:
    """Remove obviously malicious retrieved content.

    chunks: list of (source, text)
    """

    safe: List[tuple[str, str]] = []
    for source, text in chunks:
        if not allowlisted_source(source):
            continue

        # If the retrieved chunk looks like an instruction to override behavior, drop it.
        res = check_prompt_injection(text)
        if res.ok:
            safe.append((source, text))
    return safe
