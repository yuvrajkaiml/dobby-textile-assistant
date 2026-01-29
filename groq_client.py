"""
Legacy module for backward compatibility.
New code should use llm_provider.LLMProviderFactory directly.
"""

from llm_provider import LLMProviderFactory
from config import get_provider_name


def get_response(messages):
    """
    Get a response from the configured LLM provider.
    Uses the provider set in LLM_PROVIDER environment variable (default: 'groq').
    """
    provider_name = get_provider_name()
    provider = LLMProviderFactory.get_provider(provider_name)
    return provider.get_response(messages)
