"""Shared Speech-to-Text (STT) utilities for voice agents.

This package centralizes STT integrations so that multiple voice agents can
reuse the same provider-specific setup logic.
"""

from __future__ import annotations

_LAZY_EXPORTS = {
    "build_assemblyai_stt": (".assemblyai", "build_assemblyai_stt"),
    "DeepgramConfig": (".deepgram", "DeepgramConfig"),
    "build_deepgram_stt": (".deepgram", "build_deepgram_stt"),
    "build_google_stt": (".google", "build_google_stt"),
    "build_openai_stt": (".openai", "build_openai_stt"),
    "SarvamConfig": (".sarvam", "SarvamConfig"),
    "build_sarvam_stt": (".sarvam", "build_sarvam_stt"),
    "get_sarvam_language": (".sarvam", "get_sarvam_language"),
    "SonioxConfig": (".soniox", "SonioxConfig"),
    "build_soniox_stt": (".soniox", "build_soniox_stt"),
    "Transcription": (".transcribe", "Transcription"),
    "TranscriptionError": (".transcribe", "TranscriptionError"),
    "transcribe_audio": (".transcribe", "transcribe_audio"),
}


def __getattr__(name: str):
    """Load provider-specific STT modules only when their exports are used."""
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr_name = _LAZY_EXPORTS[name]
    from importlib import import_module

    value = getattr(import_module(module_name, __name__), attr_name)
    globals()[name] = value
    return value

__all__ = [
    # One-shot (push-to-talk) transcription
    "Transcription",
    "TranscriptionError",
    "transcribe_audio",
    # AssemblyAI
    "build_assemblyai_stt",
    # Deepgram
    "DeepgramConfig",
    "build_deepgram_stt",
    # Google
    "build_google_stt",
    # OpenAI
    "build_openai_stt",
    # Sarvam
    "SarvamConfig",
    "build_sarvam_stt",
    "get_sarvam_language",
    # Soniox
    "SonioxConfig",
    "build_soniox_stt",
]
