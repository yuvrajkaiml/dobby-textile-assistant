"""
Abstract LLM Provider interface and factory for provider-agnostic LLM calls.
Supports Groq, OpenAI, Anthropic, and other providers with a consistent interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Get a response from the LLM.

        Args:
            messages: List of message dicts with 'role' and 'content' keys.
                     Should include system message as first message with role='system'.

        Returns:
            str: The assistant's response text.

        Raises:
            Exception: If API call fails or required config is missing.
        """
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Return the model name/identifier."""
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """Check if provider has required configuration (API keys, etc)."""
        pass


class GroqProvider(LLMProvider):
    """Groq LLM provider implementation."""

    def __init__(self, api_key: Optional[str] = None):
        import os
        from groq import Groq

        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = "llama3-8b-8192"
        self.client = None
        if self.api_key:
            self.client = Groq(api_key=self.api_key)

    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from Groq API."""
        if not self.is_configured():
            raise ValueError("Groq API key not configured. Set GROQ_API_KEY environment variable.")
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=512
        )
        return completion.choices[0].message.content

    def get_model_name(self) -> str:
        return self.model

    def is_configured(self) -> bool:
        return self.api_key is not None


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        import os
        from openai import OpenAI

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)

    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from OpenAI API."""
        if not self.is_configured():
            raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY environment variable.")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=512
        )
        return response.choices[0].message.content

    def get_model_name(self) -> str:
        return self.model

    def is_configured(self) -> bool:
        return self.api_key is not None


class AnthropicProvider(LLMProvider):
    """Anthropic (Claude) LLM provider implementation."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        import os
        import anthropic

        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.client = None
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)

    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from Anthropic API."""
        if not self.is_configured():
            raise ValueError("Anthropic API key not configured. Set ANTHROPIC_API_KEY environment variable.")
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=512,
            messages=messages
        )
        return response.content[0].text

    def get_model_name(self) -> str:
        return self.model

    def is_configured(self) -> bool:
        return self.api_key is not None


class OpenRouterProvider(LLMProvider):
    """OpenRouter LLM provider implementation.
    
    Allows access to multiple models (Groq, OpenAI, Anthropic, etc.) via OpenRouter's unified API.
    Supports models like groq/groq-4.1-fast.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "groq/groq-4.1-fast"):
        import os
        from openai import OpenAI

        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model
        self.client = None
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.io/api/v1"
            )

    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from OpenRouter API."""
        if not self.is_configured():
            raise ValueError("OpenRouter API key not configured. Set OPENROUTER_API_KEY environment variable.")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=512
        )
        return response.choices[0].message.content

    def get_model_name(self) -> str:
        return self.model

    def is_configured(self) -> bool:
        return self.api_key is not None


class LLMProviderFactory:
    """Factory for creating and managing LLM providers."""

    _providers = {
        "groq": GroqProvider,
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "openrouter": OpenRouterProvider,
    }

    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """Register a new provider."""
        cls._providers[name.lower()] = provider_class

    @classmethod
    def get_provider(cls, provider_name: str = "groq") -> LLMProvider:
        """
        Get an LLM provider instance.

        Args:
            provider_name: Name of the provider ('groq', 'openai', 'anthropic', 'openrouter', etc).

        Returns:
            LLMProvider: Configured provider instance.

        Raises:
            ValueError: If provider name is unknown or not configured.
        """
        import os

        provider_name = provider_name.lower().strip()

        if provider_name not in cls._providers:
            available = ", ".join(cls._providers.keys())
            raise ValueError(
                f"Unknown provider '{provider_name}'. Available: {available}"
            )

        provider_class = cls._providers[provider_name]
        provider = provider_class()

        if not provider.is_configured():
            raise ValueError(
                f"Provider '{provider_name}' is not configured. "
                f"Missing API key or configuration."
            )

        return provider

    @classmethod
    def get_available_providers(cls) -> List[str]:
        """Return list of available provider names."""
        return list(cls._providers.keys())
