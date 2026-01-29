from dotenv import load_dotenv
from groq_client import get_response
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
    
    reply = get_response(messages)
    print("Bot:", reply, "\n")
    
    messages.append({"role": "assistant", "content": reply})
