from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# konteks & prompt 

konteks_gadget = "ipad pro 2021, dengan layar 12.9 inci, prosesor M1, RAM 16GB, penyimpanan 2TB, dan harga $1999."

few_shot_prompt = f"""
Tugas : ekstrak informasi dari teks ke dalam format JSON yang valid
Aturan Penting : jika informasi tidak tersedia, gunakan nilai null untuk field tersebut

contoh 1 :
teks : "Smartphone GigaPhone 15 resmi dirilis pada bulan Oktober. Ponsel ini memiliki kapasitas baterai 5000mAh dan kamera utama 108MP."
output : {{
    "nama": "GigaPhone 15",
    "rilis": "Oktober",
    "baterai": "5000mAh",
    "kamera": "108MP",
    "harga" : null
}}

sekarang giliranmu :
teks : "{konteks_gadget}"
pertanyaan : ekstrak informasi tentang nama, ukuran layar, prosesor, RAM, produk terlaris, dan harga dari teks di atas
output JSON:
"""


# Panggil API Gemini

response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents=few_shot_prompt
)

# Tampilan hasil

print("=" * 40)
print("RAW OUTPUT DARI GEMINI:")
print("=" * 40)
print(response.text)

print("\n" + "=" * 40)
print("PARSED JSON:")
print("=" * 40)
try:
    clean = response.text.strip().removeprefix(
        "```json").removeprefix("```").removesuffix("```").strip()
    data = json.loads(clean)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("\n✅ JSON valid!")
except json.JSONDecodeError as e:
    print(f"❌ JSON tidak valid: {e}")
