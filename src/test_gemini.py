import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

try:
    print("Testing Gemini connection...")
    response = model.generate_content("Say 'Connection Successful!' in one sentence.")
    print(f"Gemini says: {response.text}")
    print("\n✅ CONNECTION VERIFIED!")
except Exception as e:
    print(f"\n❌ CONNECTION FAILED: {e}")
