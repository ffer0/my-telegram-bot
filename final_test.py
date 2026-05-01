import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Читаем ключ и URL из .env
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://openai.api.proxyapi.ru/v1")

print(f"🔑 Ключ: {api_key[:15]}... (первые 15 символов)")
print(f"🌐 URL: {base_url}")

# Создаём клиента
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

# Пытаемся сгенерировать изображение
print("\n🖼️ Генерирую изображение...")
try:
    response = client.images.generate(
        model="dall-e-3",
        prompt="sunset over the sea",
        n=1,
        size="1024x1024"
    )
    print("\n✅ УСПЕХ! Ссылка на картинку:")
    print(response.data[0].url)
except Exception as e:
    print(f"\n❌ ОШИБКА: {e}")