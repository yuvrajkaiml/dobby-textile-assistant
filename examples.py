"""
Example usage of the provider-agnostic LLM architecture.
Demonstrates switching between providers and testing models.

All environment variables (API keys) are loaded from .env via python-dotenv.
No API keys are hardcoded in this file.
"""

from dotenv import load_dotenv
from llm_provider import LLMProviderFactory
from config import SYSTEM_PROMPT, set_provider_name

# Load environment variables from .env file
load_dotenv()


def example_single_provider():
    """Use a single provider to get a response."""
    print("=" * 60)
    print("Example 1: Single Provider")
    print("=" * 60)

    provider = LLMProviderFactory.get_provider('groq')
    print(f"Provider: {provider.get_model_name()}")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "What's the difference between warp and weft in yarn-dyed fabrics?"}
    ]

    response = provider.get_response(messages)
    print(f"\nResponse:\n{response}\n")


def example_multiple_providers():
    """Compare responses from different providers."""
    print("=" * 60)
    print("Example 2: Multiple Providers Comparison")
    print("=" * 60)

    question = "How does stripe width affect visual density in dobby patterns?"
    providers_to_test = ['groq', 'openai', 'anthropic', 'openrouter']

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    for provider_name in providers_to_test:
        try:
            provider = LLMProviderFactory.get_provider(provider_name)
            print(f"\n--- {provider.get_model_name()} ---")
            response = provider.get_response(messages)
            print(response)
        except ValueError as e:
            print(f"\n--- {provider_name} ---")
            print(f"⚠️  Not configured: {e}")


def example_switch_provider_at_runtime():
    """Switch providers at runtime."""
    print("=" * 60)
    print("Example 3: Runtime Provider Switching")
    print("=" * 60)

    question = "Explain dobby pattern constraints."

    # Use Groq first
    set_provider_name('groq')
    provider = LLMProviderFactory.get_provider('groq')
    print(f"Using: {provider.get_model_name()}")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]
    response = provider.get_response(messages)
    print(f"Groq response:\n{response}\n")

    # Switch to OpenAI
    set_provider_name('openai')
    try:
        provider = LLMProviderFactory.get_provider('openai')
        print(f"Switched to: {provider.get_model_name()}")
        response = provider.get_response(messages)
        print(f"OpenAI response:\n{response}\n")
    except ValueError as e:
        print(f"Could not switch to OpenAI: {e}\n")


def example_custom_provider():
    """Extend the architecture with a custom provider."""
    print("=" * 60)
    print("Example 4: Custom Provider")
    print("=" * 60)

    from llm_provider import LLMProvider

    class MockProvider(LLMProvider):
        """Mock provider for testing without real API calls."""

        def get_response(self, messages):
            user_message = next(
                (m['content'] for m in messages if m['role'] == 'user'),
                'No question'
            )
            return f"[Mock Response] You asked: {user_message}"

        def get_model_name(self):
            return "mock-model"

        def is_configured(self):
            return True

    # Register the custom provider
    LLMProviderFactory.register_provider('mock', MockProvider)

    # Use it
    provider = LLMProviderFactory.get_provider('mock')
    messages = [
        {"role": "user", "content": "Tell me about checks patterns."}
    ]
    response = provider.get_response(messages)
    print(f"Custom provider response:\n{response}\n")


if __name__ == '__main__':
    try:
        print("\n🧵 Dobby Textile Design Assistant - Provider Examples\n")

        # Uncomment examples to run them
        example_single_provider()
        example_multiple_providers()
        example_switch_provider_at_runtime()
        example_custom_provider()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
