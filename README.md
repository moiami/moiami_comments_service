# Moiami Comments Service

Flask-микросервис для комментариев и лайков

## Стек

- Flask
- PostgreSQL

## Запуск

```bash
docker compose up --build
```

Сервис поднимется на порту `8007`


## Установить зависимости

```bash
uv sync --dev
```

## Запустить юнит-тесты

```bash
uv run pytest tests -vv
```

## API (comments)

### POST /api/v1/comments

Создать комментарий

Body:
- `text` (string)
- `user_id` (UUID)
- `movie_id` (UUID)

Статусы: `201`, `400`

### GET /api/v1/comments/{comment_id}

Получить комментарий по его id

Path:
- `comment_id` (UUID)

Статусы: `200`, `404`


### PUT /api/v1/comments/{comment_id}

Обновить комментарий.
Обновлять может только владелец

Path:
- `comment_id` (UUID)

Body:
- `user_id` (UUID)
- `text` (string, опциональное поле)

Статусы: `200`, `400`, `403`, `404`

### DELETE /api/v1/comments/{comment_id}

Удалить комментарий.
Удалять может только владелец

Path:
- `comment_id` (UUID)

Body:
- `user_id` (UUID)

Статусы: `200`, `400`, `403`, `404`


## API (likes)


### POST /api/v1/comments/{comment_id}/likes

Поставить лайк на комментарий

Path:
- `comment_id` (UUID)

Body:
- `user_id` (UUID)
- `comment_id` (UUID)

Статусы: `201`, `400`, `409`


### GET /api/v1/comments/{comment_id}/likes

Получить лайки комментария

Path:
- `comment_id` (UUID)

Статусы: `200`


### DELETE /api/v1/comments/{comment_id}/likes

Удалить свой лайк с комментария

Path:
- `comment_id` (UUID)

Body:
- `user_id` (UUID)

Статусы: `200`, `400`, `404`