import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

print("Testing Gemini with detailed debug...")
print(f"API Key configured: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
print(f"API Key (first 10 chars): {os.getenv('GEMINI_API_KEY')[:10]}...")

try:
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    print("\nAvailable models:")
    for m in genai.list_models():
        print(f"  - {m.name}")
    
    print("\nTesting with gemini-1.5-flash...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello")
    print(f"Success! Response: {response.text}")
    
except Exception as e:
    print(f"\nError: {type(e).__name__}")
    print(f"Message: {e}")
    print(f"Full details: {repr(e)}")
