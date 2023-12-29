CREATE TABLE IF NOT EXISTS user_records (
    id uuid PRIMARY KEY,
    telegramId integer NOT NULL,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    date timestamp with time zone NOT NULL
);