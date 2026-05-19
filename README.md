# Moiami Comments Service

Flask-микросервис для комментариев и лайков к фильмам.

## Стек

- Flask
- SQLAlchemy / Marshmallow
- PostgreSQL
- Flasgger (Swagger UI)

## Запуск

```bash
docker compose up --build
```

Сервис поднимется на порту `8007`.

## Установить зависимости

```bash
uv sync --dev
```

## Запустить тесты

```bash
uv run pytest tests -vv
```

## Swagger UI

После запуска интерактивная документация доступна по адресу:

- http://localhost:8007/apidocs/

В Swagger описаны схемы запросов и ответов с примерами для каждой ручки.

## Формат ошибок

При ошибках сервис возвращает JSON:

```json
{
  "error": "service_error",
  "message": "описание ошибки"
}
```

## Модель комментария

Поля объекта `Comment` в ответах:

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | UUID | Идентификатор комментария |
| `text` | string | Текст комментария |
| `user_id` | UUID | Автор комментария |
| `movie_id` | UUID | Фильм, к которому относится комментарий |
| `hide` | boolean | Скрыт ли комментарий (`true` после вызова hide) |

## API (comments)

Базовый префикс: `/api/v1/comments`

### GET /api/v1/comments

Получить список всех комментариев.

Статусы: `200`, `404` (если в базе нет ни одного комментария)

Пример ответа `200`:

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "text": "Nice movie",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "movie_id": "550e8400-e29b-41d4-a716-446655440001",
    "hide": false
  }
]
```

### POST /api/v1/comments

Создать комментарий.

Body:

- `text` (string, обязательное)
- `user_id` (UUID, обязательное)
- `movie_id` (UUID, обязательное)

Статусы: `201`, `400`

Пример запроса:

```json
{
  "text": "Nice movie",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "movie_id": "550e8400-e29b-41d4-a716-446655440001"
}
```

Пример ответа `201` — объект `Comment` (см. таблицу выше).

### POST /api/v1/comments/hide/{comment_id}

Скрыть комментарий (устанавливает `hide: true`).

Path:

- `comment_id` (UUID)

Статусы: `200`, `400` (комментарий не найден)

Пример ответа `200`:

```json
{
  "message": "comment was hidden"
}
```

### GET /api/v1/comments/{comment_id}

Получить комментарий по id.

Path:

- `comment_id` (UUID)

Статусы: `200`, `400`, `404`

### PUT /api/v1/comments/{comment_id}

Обновить комментарий. Обновлять может только владелец (`user_id` в body должен совпадать с автором).

Path:

- `comment_id` (UUID)

Body:

- `user_id` (UUID, обязательное)
- `text` (string, опциональное)

Статусы: `200`, `400`, `403`, `404`

Пример запроса:

```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "text": "Updated text"
}
```

### DELETE /api/v1/comments/{comment_id}

Удалить комментарий. Удалять может только владелец.

Path:

- `comment_id` (UUID)

Body:

- `user_id` (UUID)

Статусы: `200`, `400`, `403`, `404`

Пример ответа `200`:

```json
{
  "message": "deleted"
}
```

## API (likes)

### POST /api/v1/comments/{comment_id}/likes

Поставить лайк на комментарий.

Path:

- `comment_id` (UUID) — комментарий, которому ставится лайк

Body:

- `user_id` (UUID) — пользователь, который ставит лайк

Статусы: `201`, `400`, `409` (повторный лайк от того же пользователя)

Пример запроса:

```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

Пример ответа `201`:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440020",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "comment_id": "550e8400-e29b-41d4-a716-446655440010",
  "comment": {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "text": "Nice movie",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "movie_id": "550e8400-e29b-41d4-a716-446655440001",
    "hide": false
  }
}
```

### GET /api/v1/comments/{comment_id}/likes

Получить все лайки комментария.

Path:

- `comment_id` (UUID)

Статусы: `200` (может вернуть пустой массив `[]`)

### GET /api/v1/comments/{comment_id}/likes/count

Получить количество лайков комментария.

Path:

- `comment_id` (UUID)

Пример ответа `200`:

```json
{
  "likes_count": 2
}
```

Статусы: `200`, `404` (комментарий не найден)

### DELETE /api/v1/comments/{comment_id}/likes

Удалить свой лайк с комментария.

Path:

- `comment_id` (UUID)

Body:

- `user_id` (UUID)

Статусы: `200`, `400`, `404` (лайк не найден)

Пример ответа `200`:

```json
{
  "message": "deleted"
}
```
