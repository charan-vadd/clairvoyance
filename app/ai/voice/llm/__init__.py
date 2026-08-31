"""Shared Large Language Model (LLM) utilities for voice agents.

This package centralizes LLM integrations so that multiple voice agents can
reuse the same provider-specific setup logic.
"""

from __future__ import annotations

from .types import (
    LLMConfiguration,
    LLMProvider,
    LLMSdk,
    RealtimeConfig,
    RealtimeLLMProvider,
    ThinkingConfiguration,
)

_LAZY_EXPORTS = {
    "AzureConfig": (".azure", "AzureConfig"),
    "build_azure_llm": (".azure", "build_azure_llm"),
    "ClaudeVertexConfig": (".claude_vertex", "ClaudeVertexConfig"),
    "build_claude_vertex_llm": (".claude_vertex", "build_claude_vertex_llm"),
    "OpenAIConfig": (".openai", "OpenAIConfig"),
    "build_openai_llm": (".openai", "build_openai_llm"),
    "VertexConfig": (".vertex", "VertexConfig"),
    "build_vertex_llm": (".vertex", "build_vertex_llm"),
}


def __getattr__(name: str):
    """Load provider-specific builders only when a caller asks for them."""
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr_name = _LAZY_EXPORTS[name]
    from importlib import import_module

    value = getattr(import_module(module_name, __name__), attr_name)
    globals()[name] = value
    return value

__all__ = [
    # Types
    "LLMProvider",
    "LLMSdk",
    "LLMConfiguration",
    "RealtimeConfig",
    "RealtimeLLMProvider",
    "ThinkingConfiguration",
    # Azure
    "AzureConfig",
    "build_azure_llm",
    # Google Vertex (Gemini)
    "VertexConfig",
    "build_vertex_llm",
    # Claude on Vertex
    "ClaudeVertexConfig",
    "build_claude_vertex_llm",
    # OpenAI
    "OpenAIConfig",
    "build_openai_llm",
]
