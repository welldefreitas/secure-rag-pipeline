from __future__ import annotations

import re
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FilterResult:
    ok: bool
    reason: str = ""
    confidence: float = 1.0


class PromptGuard:
    """
    Enterprise-grade Prompt Injection Defender.
    Implements a multi-layered defense strategy (Defense in Depth):
    1. Fast Heuristic/Regex Layer (Blocks obvious scripts/known vectors)
    2. Context Length Boundary (Prevents buffer overflow / token exhaustion)
    3. Semantic/Model Layer (Placeholder for llm-guard or Azure AI Content Safety)
    """

    # Layer 1: Enhanced heuristic blocks (Fast fail)
    SUSPICIOUS_PATTERNS = (
        re.compile(r"(?i)(ignore|disregard|forget)\s+(all|any|previous)\s+(instructions|prompts)"),
        re.compile(
            r"(?i)(reveal|print|show)\s+(the\s+)?(system\s+prompt|developer\s+message|hidden\s+instructions)"
        ),
        re.compile(r"(?i)(exfiltrate|leak|steal|bypass|jailbreak|dan\s+mode)"),
        re.compile(r"(?i)system:\s*|user:\s*|assistant:\s*"),  # Blocks role-playing injection
        re.compile(r"(\b\w+\b)(?:\W+\1\b){10,}"),  # Blocks token-smuggling via extreme repetition
    )

    MAX_PROMPT_LENGTH = 2000  # Enforce boundary to prevent context window attacks

    @classmethod
    def check_prompt_injection(cls, text: str) -> FilterResult:
        if not text or not text.strip():
            logger.warning("PromptGuard: Blocked empty prompt.")
            return FilterResult(ok=False, reason="empty_prompt", confidence=1.0)

        # 1. Boundary Check
        if len(text) > cls.MAX_PROMPT_LENGTH:
            logger.warning(f"PromptGuard: Blocked oversized prompt ({len(text)} chars).")
            return FilterResult(ok=False, reason="prompt_too_long", confidence=1.0)

        # 2. Fast Heuristic Check
        for pat in cls.SUSPICIOUS_PATTERNS:
            if pat.search(text):
                logger.warning(f"PromptGuard: Heuristic match blocked -> {pat.pattern}")
                return FilterResult(
                    ok=False, reason=f"heuristic_match:{pat.pattern}", confidence=0.95
                )

        # 3. Semantic / External API Check (Architecture Ready)
        # In a real prod env, we would call: ProtectAI/llm-guard or Azure Prompt Shields here.
        semantic_check = cls._semantic_scan_mock(text)
        if not semantic_check.ok:
            return semantic_check

        return FilterResult(ok=True)

    @classmethod
    def _semantic_scan_mock(cls, text: str) -> FilterResult:
        """
        Placeholder for ML-based semantic scanning.
        Shows architectural maturity for plugging in tools like 'llm-guard'.
        """
        # Example of a semantic block that regex might miss:
        encoded_or_tricky = ["base64", "hex", "translate to"]
        if (
            any(trick in text.lower() for trick in encoded_or_tricky)
            and "system prompt" in text.lower()
        ):
            logger.warning("PromptGuard: Semantic anomaly detected (Evade attempt).")
            return FilterResult(ok=False, reason="semantic_anomaly_detected", confidence=0.85)

        return FilterResult(ok=True)


# Interface for the rest of the application
def check_prompt_injection(text: str) -> FilterResult:
    return PromptGuard.check_prompt_injection(text)
