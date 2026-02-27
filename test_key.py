from dotenv import load_dotenv
import os
import anthropic

load_dotenv()
key = os.environ.get("ANTHROPIC_API_KEY")

print(f"Key loaded: {key[:20]}..." if key else "❌ No key found")
print(f"Key length: {len(key)}" if key else "")

# Test the key with Anthropic
try:
    client = anthropic.Anthropic(api_key=key)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hi"}]
    )
    print("✅ API Key is VALID!")
    print(f"Response: {message.content[0].text}")
except Exception as e:
    print(f"❌ API Key test failed: {e}")