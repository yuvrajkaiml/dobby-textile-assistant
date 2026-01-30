from dotenv import load_dotenv
from llm_provider import LLMProviderFactory
from config import SYSTEM_PROMPT, get_provider_name

# Load environment variables from .env file
load_dotenv()

print("🤖 Dobby Textile Design Assistant started (type 'exit' to quit)")
print(f"   Using provider: {get_provider_name()}\n")

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "exit":
        print("Goodbye 👋")
        break
    
    messages.append({"role": "user", "content": user_input})
    
    provider_name = get_provider_name()
    provider = LLMProviderFactory.get_provider(provider_name)
    reply = provider.get_response(messages)
    print("Bot:", reply, "\n")
    
    messages.append({"role": "assistant", "content": reply})
