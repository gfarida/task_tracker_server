# Task Tracker API

**Task Tracker** — это API-сервис для управления задачами, позволяющий пользователям регистрироваться, авторизоваться и работать со своими личными списками задач. Сервис предоставляет удобный REST API для создания, редактирования, просмотра и удаления задач.



## Основные возможности

- Регистрация и вход по логину/паролю
- Создание, обновление, удаление и просмотр задач
- Привязка задач к конкретному пользователю
- Аутентификация через JWT-токены
- Swagger UI-документация по адресу `/docs`

## Используемые технологии

- **FastAPI** – создание REST API
- **Uvicorn** – ASGI-сервер для запуска приложения
- **SQLite** – встроенная база данных
- **SQLAlchemy** – ORM для работы с БД
- **Pydantic** – валидация и сериализация данных


## Запуск сервера

1. Соберите образ:
   ```bash
   cd task_tracker_server
   docker build -t task_tracker_server .
   ```

2. Запустите контейнер:

    ```bash
    docker run -p 80:80 task_tracker_server
    ```

3. Откройте в браузере:

    ```bash
    http://localhost/docs
    ```

## Возможности API

### Аутентификация (`/auth`)

1. `POST /auth/register` - создаёт нового пользователя.

    Request:
    ```json
    {
        "username": "user",
        "password": "password"
    }
    ```

    Response:

    ```json
    {
        "id": 1,
        "username": "user"
    }
    ```

2. `POST /auth/login` - Выполняет вход и возвращает JWT-токен для дальнейшей аутентификации.

    Request:

    Параметры (form):

    - `username`: логин пользователя
    - `password`: пароль пользователя

    Response:

    ```json
    {
        "access_token": "<JWT_TOKEN>",
        "token_type": "bearer"
    }
    ```

### Задачи (/tasks)
Все запросы к этим эндпоинтам требуют авторизации через Authorization: Bearer <token>.

1. `POST /tasks` - создаёт новую задачу.

    Request:

    ```json
    {
        "name": "task1",
        "description": "desc1"
    }
    ```

    Response:

    ```json
    {
        "ok": true,
        "task_id": 5
    }
    ```

2. `GET /tasks` - получает список задач текущего пользователя. Поддерживает пагинацию и фильтрацию по названию.

    Query параметры:

    - `limit`: количество задач (по умолчанию 10)

    - `offset`: смещение (по умолчанию 10)

    - `name`: фильтр по названию задачи (опционально)

    Response:

    ```json
    [
        {
            "name": "task1",
            "description": "desc1",
            "id": 1
        },
        {
            "name": "task2",
            "description": "desc2",
            "id": 2
        },
        ...
    ]
    ```

3. `DELETE /tasks/{task_id}` - удаляет задачу по ID.

    Path параметр:

    - `task_id`: ID задачи для удаления

    Response:

    ```json
    {
        "ok": true
    }
    ```
