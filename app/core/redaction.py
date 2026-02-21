from __future__ import annotations

import logging

# Enterprise Standard for PII Redaction: Microsoft Presidio
try:
    from presidio_analyzer import AnalyzerEngine
    from presidio_anonymizer import AnonymizerEngine

    PRESIDIO_AVAILABLE = True
except ImportError:
    PRESIDIO_AVAILABLE = False

logger = logging.getLogger(__name__)


class PIIRedactor:
    """
    Enterprise PII Redaction Engine using Microsoft Presidio (NLP + Regex).
    Falls back to basic Regex if Presidio is not installed (e.g., lightweight environments).
    """

    def __init__(self):
        self.use_presidio = PRESIDIO_AVAILABLE
        if self.use_presidio:
            logger.info("Initializing Microsoft Presidio for NLP-based PII Redaction.")
            self.analyzer = AnalyzerEngine()
            self.anonymizer = AnonymizerEngine()
        else:
            logger.warning(
                "Presidio not found. Falling back to basic Regex. "
                "Install 'presidio-analyzer' and 'presidio-anonymizer' for production."
            )

    def redact(self, text: str) -> str:
        if not text or not text.strip():
            return text

        if self.use_presidio:
            return self._redact_presidio(text)
        return self._redact_regex_fallback(text)

    def _redact_presidio(self, text: str) -> str:
        # Presidio automatically detects PERSON, LOCATION, EMAIL, PHONE_NUMBER, etc.
        try:
            results = self.analyzer.analyze(text=text, entities=[], language="en")
            anonymized = self.anonymizer.anonymize(text=text, analyzer_results=results)
            return anonymized.text
        except Exception as e:
            logger.error(f"Presidio redaction failed: {e}. Returning safely redacted text.")
            return "[REDACTION_ERROR - CONTENT BLOCKED]"

    def _redact_regex_fallback(self, text: str) -> str:
        """Basic fallback when Presidio is not available."""
        import re

        redacted = text
        # Simple Email Regex
        redacted = re.sub(
            r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "[EMAIL]", redacted, flags=re.IGNORECASE
        )
        # Simple Credit Card Regex
        redacted = re.sub(r"\b(?:\d[ -]*?){13,19}\b", "[CARD]", redacted)
        # AWS Key Regex
        redacted = re.sub(r"\bAKIA[0-9A-Z]{16}\b", "[AWS_KEY]", redacted)
        return redacted


# Singleton instance
_redactor = PIIRedactor()


def redact_text(text: str) -> str:
    return _redactor.redact(text)
