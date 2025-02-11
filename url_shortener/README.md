# 🚀 Flask URL Shortener & Telegram Bot Integration

![Flask](https://img.shields.io/badge/Flask-v2.2.2-blue) 
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-green)
![Python](https://img.shields.io/badge/Python-3.10-yellow)

Добро пожаловать в репозиторий, где собрано всё для создания удобного сервиса сокращения ссылок с использованием **Flask** и интеграции с Telegram-ботом!  

---

## 📁 Структура проекта

- **`bin/`**  
  Все тестовые файлы и черновой код находятся здесь — это наша песочница.

- **`url_shortener/`**  
  Главная директория проекта, где содержится рабочий код сокращателя ссылок на Flask.

  - `app.py` — основной файл приложения.  
  - `templates/` — HTML-шаблоны для интерфейса (если потребуется).  
  - `static/` — CSS, JS и другие статические файлы.  
  - `database/` — используется для хранения ссылок и статистики.  

---

## 🧩 Реализованные функции

1. **Сокращение ссылок через Flask**  
   Используйте API для создания коротких ссылок и получения статистики.

2. **Telegram-бот**  
   - Сокращает ссылки по запросу.  
   - Отправляет статистику по коротким ссылкам.  
   - Ограничение на доступ к статистике (белый список).

3. **Работа с `curl`**  
   Для проверки и взаимодействия с API без использования интерфейса.

---

## 🔧 Пример использования API

### Сокращение ссылки
```bash
curl -X POST http://127.0.0.1:5000/shorten -H "Content-Type: application/json" -d '{"original_url": "https://example.com"}'
```

**Ответ:**
```json
{
  "short_url": "http://127.0.0.1:5000/abc123",
  "original_url": "https://example.com"
}
```

### Получение статистики
```bash
curl -X GET http://127.0.0.1:5000/stats/abc123
```

**Ответ:**
```json
{
  "short_id": "abc123",
  "original_url": "https://example.com",
  "clicks": 42
}
```

---

## 🤖 Telegram Bot Команды

- **`/start`** — Начать работу с ботом.  
- **Сокращение ссылки:** отправьте ссылку напрямую, и бот сократит её.  
- **Получение статистики:** отправьте короткую ссылку (доступно для избранных пользователей).  

---

## 📦 Установка и запуск

### Шаг 1: Клонирование репозитория
```bash
git clone https://github.com/your-username/url-shortener-bot.git
cd url-shortener-bot
```

### Шаг 2: Установка зависимостей
```bash
pip install -r requirements.txt
```

### Шаг 3: Запуск Flask-сервера
```bash
cd url_shortener
python app.py
```

### Шаг 4: Запуск Telegram-бота
Создайте файл `config.py` с токеном вашего бота:
```python
bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
api_url = "http://127.0.0.1:5000"
whitelist = [123456789, 987654321]  # Telegram ID разрешённых пользователей
```

```bash
python bot.py
```

---

## 🛠️ Планы на будущее

- Добавить графический интерфейс для веб-приложения.  
- Реализовать аналитику для ссылок (история переходов, география и т.д.).  
- Интеграция с другими популярными мессенджерами.  
- Новый проект: **"Продолжение следует..."**

---

### 🌟 Поддержите проект
Если вам понравился проект или он оказался полезен, поставьте ⭐ на репозитории! 😊



