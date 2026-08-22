# Data Quality Monitor (DQM)

Легковесный веб-сервис на Flask для автоматического мониторинга качества данных в реляционных базах данных. Приложение в реальном времени проверяет полноту данных (отсутствие `NULL`), рассчитывает метрики качества, отображает результаты на интерактивном дашборде и отправляет уведомления в Telegram при обнаружении аномалий.

---

### Key Features

* **Автоматический инспектор БД:** Сканирование таблиц, подсчет записей, обнаружение незапланированных `NULL`-значений и расчет метрики **Completeness Score ($CS$)**.
* **Интерактивный дашборд:** Наглядная визуализация статусов таблиц, детализации по проблемным столбцам и динамических графиков (Bootstrap 5 + Chart.js).
* **Гибкий алертинг:** Интеграция с Telegram Bot API для отправки мгновенных алертов при падении полноты данных ниже заданного порога (по умолчанию $< 90\%$).
* **REST API:** Набор эндпоинтов для интеграции с внешней инфраструктурой и CI/CD:
  * `GET /api/v1/healthcheck` — проверка подключения к базе данных.
  * `POST /api/v1/scan` — запуск сканирования с отправкой алертов.
  * `GET /api/v1/run-tests` — запуск юнит-тестов прямо из веб-приложения.
* **Генератор отчетов:** Автоматическое создание графиков высокой точности и сводных отчетов в форматах PDF/Markdown для презентации.
* **Система аудита:** Встроенный скрипт диагностики для быстрой проверки целостности всех компонентов.

---

### Архитектура системы

```text
[ PostgreSQL / MySQL / SQLite ] 
               │
               ▼ (SQLAlchemy ORM Inspection)
┌──────────────────────────────────────────┐
│        Data Quality Engine (Flask)       │
│  - DB Inspector (Подсчет COUNT, NULL)    │
│  - Metrics Calculator (Completeness Score│
│  - Alerting Engine (Telegram Notifier)   │
└────────────────────┬─────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌───────────────┐        ┌──────────────────┐
│ Web Dashboard │        │  Telegram / API  │
│ (Chart.js /   │        │   Notification   │
│  Bootstrap 5) │        │   (/api/v1/scan) │
└───────────────┘        └──────────────────┘

```

---

### Структура проекта

```text
├── app/
│   ├── __init__.py          # Инициализация Flask-приложения
│   ├── config.py            # Конфигурация и подключение к БД
│   ├── inspector.py         # Модуль сбора метрик и сканирования БД
│   ├── alerts.py            # Модуль отправки алертов в Telegram
│   ├── bot_setup.py         # Авто-проверка и инициализация Telegram-бота
│   ├── routes.py            # Маршруты веб-интерфейса и REST API
│   ├── templates/           # HTML-шаблоны Jinja2 (dashboard.html)
│   └── static/              # Стили оформления (style.css)
├── tests/
│   └── test_inspector.py    # Юнит-тесты на Pytest
├── instance/                # Локальная база данных SQLite (test_data.db)
├── create_test_db.py        # Генератор тестовой БД (clean, warning, critical)
├── generate_report_assets.py# Генератор графиков и отчетов для презентации
├── audit_project.py         # Скрипт полной проверки и диагностики проекта
├── main.py                  # Главная точка входа приложения
├── requirements.txt         # Фиксированные зависимости проекта
├── .env                     # Переменные окружения (конфиденциальные ключи)
└── README.md                # Полное техническое руководство

```

---

### Настройка интеграции с Telegram

Для получения мгновенных уведомлений об аномалиях в БД необходимо настроить Telegram-бота.

#### 1. Создание бота и получение токена

1. Перейдите в Telegram к боту **[@BotFather](https://t.me/BotFather)**.
2. Отправьте команду `/newbot` и следуйте инструкциям:
* Укажите имя бота (например, `DQM Monitor`).
* Укажите юзернейм (должен оканчиваться на `bot`, например, `my_dqm_system_bot`).


3. Скопируйте предоставленный **HTTP API Token** (формат: `1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ`).

#### 2. Получение `CHAT_ID`

1. Найдите бота **[@userinfobot](https://t.me/userinfobot)** и нажмите **Start**.
2. Скопируйте ваш персональный `Id` (например, `123456789`).
3. Перейдите к созданному боту и обязательно нажмите **Start** (чтобы разрешить отправку сообщений).

> **Примечание:** Для отправки алертов в групповой чат добавьте бота в группу, назначьте администратором и узнайте ID группы через `@myidbot` (ID группы начинается со знака минус, например `-100123456789`).

#### 3. Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта и укажите ключи (они будут автоматически загружены через `python-dotenv` при старте приложения):

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ
TELEGRAM_CHAT_ID=123456789

```

#### 4. Проверка интеграции

Выполните команду для проверки доставки тестового сообщения:

```bash
python -c "from app.alerts import TelegramNotifier; TelegramNotifier().send_alert('🚀 <b>DQM System</b>: Настройка прошла успешно!')"

```

---

### Быстрый запуск

**1. Клонирование репозитория и настройка окружения:**

```bash
git clone [https://github.com/your-username/Data-monitoring-system-in-the-database-Flask-.git](https://github.com/your-username/Data-monitoring-system-in-the-database-Flask-.git)
cd Data-monitoring-system-in-the-database-Flask-

python -m venv .venv
source .venv/bin/activate  # Для Linux/macOS
# .venv\Scripts\activate   # Для Windows

```

**2. Установка зависимостей:**

```bash
pip install -r requirements.txt

```

**3. Создание тестовой базы данных:**

```bash
python create_test_db.py

```

**4. Запуск веб-приложения:**

```bash
python main.py

```

После запуска откройте браузер по адресу: `http://127.0.0.1:5000/`.

---

### Диагностика, тесты и генерация материалов

* **Полный аудит проекта:**
```bash
python audit_project.py

```


*Генерирует лог `project_audit.log` с проверкой всех файлов, пакетов, БД и тестов.*
* **Запуск юнит-тестов:**
```bash
pytest

```


* **Генерация презентационных материалов (графики, Markdown-таблицы и PDF):**
```bash
python generate_report_assets.py

```


Все сгенерированные файлы будут сохранены в папке `presentation_assets/`.

---

### Стек технологий

* **Backend:** Python 3.12, Flask 3.0, SQLAlchemy 2.0, python-dotenv
* **Frontend:** Bootstrap 5, Chart.js, Jinja2
* **Testing & Quality:** Pytest 8.0
* **Analytics & Visualization:** Pandas, Seaborn, Matplotlib

```

```
