import os
from openai import OpenAI
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# 1. ПРОВЕРЯЕМ, ЧТО ЗАГРУЗИЛОСЬ
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://openai.api.proxyapi.ru/v1")

print(f"🔑 Ключ API загружен: {'Да (начинается с ' + api_key[:7] + '...)' if api_key else 'НЕТ!'}")
print(f"🌐 Базовый URL: {base_url}")

# Создаём клиента
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

# 2. ПЫТАЕМСЯ ПОЛУЧИТЬ СПИСОК МОДЕЛЕЙ (для диагностики)
print("\n--- Проверка подключения ---")
try:
    models = client.models.list()
    print("✅ Соединение установлено! Список моделей получен.")
    # Выведем первые 3 модели, чтобы убедиться
    for m in list(models)[:3]:
        print(f"  - {m.id}")
except Exception as e:
    print(f"❌ Ошибка при подключении или получении списка моделей: {type(e).__name__}: {e}")

# 3. ПЫТАЕМСЯ СГЕНЕРИРОВАТЬ ИЗОБРАЖЕНИЕ
print("\n--- Попытка генерации изображения ---")
try:
    response = client.images.generate(
        model="dall-e-3",  # Попробуйте также "openai/dall-e-3", если эта не сработает
        prompt="a simple red flower on a white background",
        n=1,
        size="1024x1024"
    )
    print("✅ Успех! Изображение сгенерировано. Ссылка:")
    print(response.data[0].url)
except Exception as e:
    print(f"❌ Ошибка генерации: {type(e).__name__}: {e}")