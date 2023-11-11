DROP TABLE IF EXISTS fitbit_auth;

CREATE TABLE fitbit_auth (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    access_token TEXT NOT NULL
);