import requests
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://openai.api.proxyapi.ru/v1"

# Проверяем, что ключ загрузился
print(f"🔑 Используется API-ключ: {API_KEY[:15]}..." if API_KEY else "❌ Ключ не загружен!")
print(f"🌐 URL: {BASE_URL}")

# Формируем запрос к эндпоинту /chat/completions
url = f"{BASE_URL}/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Пробуем вызвать модель через стандартный чат-интерфейс
payload = {
    "model": "gpt-3.5-turbo",  # самая простая и дешёвая модель для проверки
    "messages": [
        {"role": "user", "content": "Say 'API works!'"}
    ],
    "max_tokens": 20
}

print("\n📡 Отправляю тестовый запрос к /chat/completions...")
try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"📊 Статус-код: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ УСПЕХ! API работает.")
        print("📨 Ответ:", response.json()["choices"][0]["message"]["content"])
    else:
        print(f"❌ ОШИБКА: {response.status_code}")
        print("📨 Тело ответа:", response.text)
        
except Exception as e:
    print(f"❌ Исключение: {e}")