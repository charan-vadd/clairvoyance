"""Shared Text-to-Speech (TTS) utilities for voice agents.

This package centralizes TTS integrations so that multiple voice agents can
reuse the same provider-specific setup logic.
"""

from __future__ import annotations

_LAZY_EXPORTS = {
    "CartesiaConfig": (".cartesia", "CartesiaConfig"),
    "build_cartesia_tts": (".cartesia", "build_cartesia_tts"),
    "DragonTTSConfig": (".dragontts", "DragonTTSConfig"),
    "build_dragontts_tts": (".dragontts", "build_dragontts_tts"),
    "ElevenLabsConfig": (".elevenlabs", "ElevenLabsConfig"),
    "build_elevenlabs_tts": (".elevenlabs", "build_elevenlabs_tts"),
    "GeminiConfig": (".gemini", "GeminiConfig"),
    "build_gemini_tts": (".gemini", "build_gemini_tts"),
    "GoogleConfig": (".google", "GoogleConfig"),
    "build_google_tts": (".google", "build_google_tts"),
    "SarvamTTSConfig": (".sarvam", "SarvamTTSConfig"),
    "build_sarvam_tts": (".sarvam", "build_sarvam_tts"),
    "get_sarvam_language": (".sarvam", "get_sarvam_language"),
    "SonioxTTSConfig": (".soniox", "SonioxTTSConfig"),
    "build_soniox_tts": (".soniox", "build_soniox_tts"),
}


def __getattr__(name: str):
    """Load provider-specific TTS modules only when their exports are used."""
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr_name = _LAZY_EXPORTS[name]
    from importlib import import_module

    value = getattr(import_module(module_name, __name__), attr_name)
    globals()[name] = value
    return value

__all__ = [
    # Cartesia
    "CartesiaConfig",
    "build_cartesia_tts",
    # DragonTTS (caching proxy)
    "DragonTTSConfig",
    "build_dragontts_tts",
    # ElevenLabs
    "ElevenLabsConfig",
    "build_elevenlabs_tts",
    # Gemini
    "GeminiConfig",
    "build_gemini_tts",
    # Google (Chirp3 HD)
    "GoogleConfig",
    "build_google_tts",
    # Sarvam
    "SarvamTTSConfig",
    "build_sarvam_tts",
    "get_sarvam_language",
    # Soniox
    "SonioxTTSConfig",
    "build_soniox_tts",
]
