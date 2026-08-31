"""Breeze Buddy custom processors for pipeline control."""

from importlib import import_module
from typing import Any

__all__ = [
    "KnowledgeRetrievalProcessor",
    "MetricsCollectorProcessor",
    "TranscriptCollectorProcessor",
    "TranscriptionGateProcessor",
    "UserIdleCallbackHandler",
    "VoiceUiStreamProcessor",
]

_LAZY_EXPORTS = {
    "KnowledgeRetrievalProcessor": (
        "app.ai.voice.agents.breeze_buddy.processors.knowledge_retrieval"
    ),
    "MetricsCollectorProcessor": (
        "app.ai.voice.agents.breeze_buddy.processors.metrics_collector_processor"
    ),
    "TranscriptCollectorProcessor": (
        "app.ai.voice.agents.breeze_buddy.processors.transcript_collector"
    ),
    "TranscriptionGateProcessor": (
        "app.ai.voice.agents.breeze_buddy.processors.transcription_gate"
    ),
    "UserIdleCallbackHandler": (
        "app.ai.voice.agents.breeze_buddy.processors.user_idle"
    ),
    "VoiceUiStreamProcessor": (
        "app.ai.voice.agents.breeze_buddy.processors.voice_ui_stream"
    ),
}


def __getattr__(name: str) -> Any:
    module_path = _LAZY_EXPORTS.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module(module_path), name)
    globals()[name] = value
    return value
