# modules/get_free_keys.py
import webbrowser

def show_free_api_guide():
    print("="*60)
    print("🔑 GET FREE AI API KEYS")
    print("="*60)
    
    services = {
        "1. Google Gemini": {
            "url": "https://makersuite.google.com/app/apikey",
            "free_tier": "60 requests per minute",
            "steps": [
                "1. Go to the link above",
                "2. Sign in with Google account",
                "3. Create new API key",
                "4. Copy the key",
                "5. Add to .env: GEMINI_API_KEY=your_key"
            ]
        },
        "2. DeepSeek": {
            "url": "https://platform.deepseek.com/api_keys",
            "free_tier": "Free with rate limits",
            "steps": [
                "1. Sign up at DeepSeek",
                "2. Go to API Keys section",
                "3. Create new key",
                "4. Copy the key",
                "5. Add to .env: DEEPSEEK_API_KEY=your_key"
            ]
        },
        "3. Hugging Face": {
            "url": "https://huggingface.co/settings/tokens",
            "free_tier": "Free inference API",
            "steps": [
                "1. Create Hugging Face account",
                "2. Go to Settings → Access Tokens",
                "3. Create new token",
                "4. Copy the token",
                "5. Add to .env: HUGGINGFACE_TOKEN=your_token"
            ]
        }
    }
    
    for service, info in services.items():
        print(f"\n{service}")
        print(f"📊 Free tier: {info['free_tier']}")
        print("📝 Steps:")
        for step in info['steps']:
            print(f"   {step}")
        
        open_link = input(f"\nOpen {service} website? (y/n): ")
        if open_link.lower() == 'y':
            webbrowser.open(info['url'])
    
    print("\n" + "="*60)
    print("✅ After getting keys, add them to .env file")
    print("✅ Then restart your chatbot")
    print("="*60)

if __name__ == "__main__":
    show_free_api_guide()
