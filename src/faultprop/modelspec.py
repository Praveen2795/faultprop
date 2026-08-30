"""Resolve a model spec string to a Strands model provider.

Spec format: "<provider>:<model_id>"  e.g.
    ollama:gemma4:e2b            (local, free — dev/debug)
    anthropic:claude-haiku-4-5-20251001
    openai:gpt-4o-mini
    bedrock:us.anthropic.claude-...
A bare string with no known provider prefix is passed through unchanged, so
Strands' own default (Bedrock) still works.

Keeping this in one place means the experiment grid records exactly which
backend produced each episode.
"""
from __future__ import annotations

import os

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")


def resolve(spec: str):
    provider, _, model_id = spec.partition(":")
    provider = provider.lower()

    if provider == "ollama":
        from strands.models.ollama import OllamaModel
        return OllamaModel(host=OLLAMA_HOST, model_id=model_id)

    if provider == "anthropic":
        from strands.models.anthropic import AnthropicModel
        return AnthropicModel(model_id=model_id, max_tokens=2048)

    if provider == "openai":
        from strands.models.openai import OpenAIModel
        return OpenAIModel(model_id=model_id)

    if provider == "gemini":
        from strands.models.gemini import GeminiModel
        return GeminiModel(model_id=model_id)

    if provider == "bedrock":
        from strands.models.bedrock import BedrockModel
        return BedrockModel(model_id=model_id)

    return spec  # let Strands decide
