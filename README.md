# Dobby Textile Design Assistant

A provider-agnostic LLM chatbot for yarn-dyed textile design. Easily compare responses across multiple AI providers (Groq, OpenAI, Anthropic, OpenRouter) with a consistent system prompt.

## Features

- **Provider-Agnostic**: Switch between Groq, OpenAI, Anthropic, and OpenRouter with a single environment variable
- **Secure Configuration**: API keys loaded from environment variables via `.env` file (never hardcoded)
- **Consistent Prompts**: Same system prompt across all providers for fair comparison
- **Web & CLI Interfaces**: Use the Flask web app or command-line interface
- **Easy Model Switching**: Test different models to compare response quality and speed
- **OpenRouter Support**: Access Groq (via groq-4.1-fast) and other models through OpenRouter's unified API

## Setup

```bash
# Install core dependencies
python -m pip install -r requirements.txt

# Optional: Install additional provider SDKs for model comparison
pip install openai anthropic
```

## Configuration

Set environment variables in a `.env` file (recommended) or export them. API keys are loaded securely via `python-dotenv` and never hardcoded.

### Create a `.env` file in the project root:

```bash
# Choose your default provider (default: groq)
LLM_PROVIDER=openrouter

# Set API keys for providers you'll use
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
OPENROUTER_API_KEY=your_openrouter_key

# Optional: Override model names
GROQ_MODEL=llama3-8b-8192
OPENAI_MODEL=gpt-4o-mini
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
OPENROUTER_MODEL=groq/groq-4.1-fast
```

**⚠️ Security**: Do NOT commit `.env` to source control. See `.gitignore` to ensure `.env` files are excluded.

## Running

### Web Interface (Recommended)

```bash
# Start Flask server on http://127.0.0.1:5000
python web.py
```

Visit http://127.0.0.1:5000 in your browser. The web interface displays which provider is currently active.

### CLI Interface

```bash
# Run the command-line chatbot
python app.py
```

Type 'exit' to quit.

## Switching Providers

### Via Environment Variable

```bash
# Use OpenAI instead of Groq (make sure OPENAI_API_KEY is set)
export LLM_PROVIDER=openai
python web.py
```

### Via Code

```python
from config import set_provider_name
from groq_client import get_response

# Switch to OpenRouter
set_provider_name('openrouter')

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]

response = get_response(messages)
print(response)
```

## Using OpenRouter

### Setup OpenRouter API Key

1. Sign up at [OpenRouter.ai](https://openrouter.ai)
2. Get your API key from the dashboard
3. Add it to your `.env` file:

```bash
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=groq/groq-4.1-fast
```

### Available Models on OpenRouter

- `groq/groq-4.1-fast` - Groq's fast model (default)
- `openai/gpt-4-turbo` - OpenAI's GPT-4 Turbo
- `anthropic/claude-3-sonnet` - Anthropic's Claude 3 Sonnet
- [Browse all models](https://openrouter.ai/docs#models)

### Run with OpenRouter

```bash
# Using Flask web interface
python web.py

# Using CLI
python app.py
```

The app will use OpenRouter with your configured model and API key.

## Architecture

### Provider Abstraction

The `llm_provider.py` module provides:

- **LLMProvider**: Abstract base class defining the interface
- **GroqProvider**: Groq API implementation
- **OpenAIProvider**: OpenAI API implementation
- **AnthropicProvider**: Anthropic API implementation
- **LLMProviderFactory**: Factory for creating and managing providers

### Usage Example

```python
from llm_provider import LLMProviderFactory

# Get the configured provider
provider = LLMProviderFactory.get_provider('openai')

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is 2+2?"}
]

response = provider.get_response(messages)
print(response)
```

### Extending with New Providers

Create a new provider by subclassing `LLMProvider`:

```python
from llm_provider import LLMProvider, LLMProviderFactory

class MyProvider(LLMProvider):
    def __init__(self, api_key=None):
        # Initialize your provider
        pass

    def get_response(self, messages):
        # Implement API call
        return "response"

    def get_model_name(self):
        return "my-model"

    def is_configured(self):
        return True  # Check for API key, etc.

# Register the provider
LLMProviderFactory.register_provider('myprovider', MyProvider)

# Use it
provider = LLMProviderFactory.get_provider('myprovider')
```

## Security

- **Do NOT** commit `.env` files or API keys to source control
- See `.gitignore` for excluded files
- Each API key should have appropriate rate limits and scopes set in the provider's dashboard

## Model Comparison Workflow

To compare models fairly:

1. **Use the same system prompt** - All providers use `config.SYSTEM_PROMPT`
2. **Ask identical questions** - Pose the same textile design questions
3. **Note response characteristics**:
   - Response latency
   - Answer clarity and relevance
   - Technical accuracy for textile design
   - Conciseness and structure

## Supported Providers

| Provider | Models | Status |
|----------|--------|--------|
| **Groq** | Llama 3 8B | ✅ Supported |
| **OpenAI** | GPT-4, GPT-4o, GPT-4o-mini | ✅ Supported |
| **Anthropic** | Claude 3 family | ✅ Supported |
| **OpenRouter** | Groq, OpenAI, Anthropic, and 100+ more | ✅ Supported |

## License

MIT
