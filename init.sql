CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    text VARCHAR(4000) NOT NULL,
    user_id UUID NOT NULL,
    movie_id UUID NOT NULL,
    hide BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS likes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    comment_id UUID NOT NULL REFERENCES comments(id) ON DELETE CASCADE,
    UNIQUE (user_id, comment_id)
);
