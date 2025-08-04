-- migrate:up

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    message VARCHAR(255),
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() at time zone 'Europe/Moscow')
);

-- migrate:down
DROP TABLE messages