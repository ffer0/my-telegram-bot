import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://openai.api.proxyapi.ru/v1")

print(f"🔑 Ключ: {api_key[:15]}... (первые 15 символов)")
print(f"🌐 URL: {base_url}")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

print("\n🖼️ Генерирую изображение через chat.completions...")

try:
    response = client.chat.completions.create(
        model="openai/dall-e-3",
        messages=[
            {"role": "user", "content": "Нарисуй красный цветок на белом фоне"}
        ],
        max_tokens=500
    )
    
    print("\n✅ УСПЕХ! Ответ:")
    print(response.choices[0].message.content)
    
except Exception as e:
    print(f"\n❌ ОШИБКА: {e}")