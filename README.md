# InsidersBooks API

Простий API для управління книгами з авторизацією та ролями користувачів.

## Що це таке

Це FastAPI додаток для роботи з книгами. Є три типи користувачів:
- **Reader** - може тільки дивитися книги
- **Writer** - може створювати та редагувати книги  
- **Admin** - може все + видаляти книги

## Як запустити

1. Встановити залежності:
```bash
poetry install
```

2. Запустити сервер:
```bash
poetry run uvicorn src.insidersbooks.main:app --reload
```

3. Відкрити в браузері: http://127.0.0.1:8000/docs

## Структура проекту

```
InsidersBooks/
├── src/
│   └── insidersbooks/
│       ├── main.py              # Головний файл FastAPI
│       ├── database.py          # Налаштування БД
│       ├── models/              # Моделі SQLAlchemy
│       │   ├── user.py          # Модель користувача
│       │   └── book.py          # Модель книги
│       ├── schemas/             # Pydantic схеми
│       │   ├── user.py          # Схеми для User
│       │   └── book.py          # Схеми для Book
│       ├── routes/              # API ендпоінти
│       │   ├── auth.py          # Авторизація
│       │   └── book.py          # Робота з книгами
│       └── dependencies/        # Залежності
│           └── auth.py          # Перевірка токенів і ролей
├── pyproject.toml              # Конфігурація Poetry
└── README.md
```

## API Ендпоінти

### Авторизація (`/auth`)
- `POST /auth/register` - Реєстрація нового користувача
- `POST /auth/login` - Вхід (отримання токена)
- `GET /auth/me` - Інформація про поточного користувача

### Книги (`/books`)
- `GET /books` - Список всіх книг (доступно всім)
- `GET /books/{id}` - Отримати книгу за ID
- `POST /books` - Створити нову книгу (writer/admin)
- `PUT /books/{id}` - Редагувати книгу (writer/admin)
- `DELETE /books/{id}` - Видалити книгу (тільки admin)

## Як користуватися

1. **Зареєструватися**: POST `/auth/register`
2. **Увійти**: POST `/auth/login` (отримаєш токен)
3. **Створити книгу**: POST `/books` (потрібен токен + роль writer/admin)

Токен треба вставляти в заголовок Authorization: `Bearer your_token_here`

## База даних

Використовується PostgreSQL. Налаштування в `database.py`:
```
postgresql://postgres:qwerty12345@localhost/insidersbooks_db
```

Таблиці створюються автоматично при запуску.