-- SQLite: включать для каждого подключения до начала транзакции.
PRAGMA foreign_keys = ON;

CREATE TABLE habits (
    habit_id TEXT NOT NULL PRIMARY KEY,
    title TEXT NOT NULL CHECK (length(trim(title, ' ' || char(9) || char(10) || char(13))) BETWEEN 1 AND 100),
    description TEXT CHECK (description IS NULL OR length(description) <= 500),
    created_date TEXT NOT NULL CHECK (
        length(created_date) = 10 AND created_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
        AND date(created_date, '+0 days') IS NOT NULL AND date(created_date, '+0 days') = created_date
    )
);

CREATE TABLE completions (
    habit_id TEXT NOT NULL,
    completion_date TEXT NOT NULL CHECK (
        length(completion_date) = 10 AND completion_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
        AND date(completion_date, '+0 days') IS NOT NULL AND date(completion_date, '+0 days') = completion_date
    ),
    PRIMARY KEY (habit_id, completion_date),
    FOREIGN KEY (habit_id) REFERENCES habits (habit_id) ON DELETE CASCADE
);

CREATE INDEX idx_habits_created_date ON habits (created_date);
CREATE INDEX idx_completions_date ON completions (completion_date);

CREATE TRIGGER completions_check_start_insert
BEFORE INSERT ON completions
WHEN EXISTS (SELECT 1 FROM habits WHERE habit_id = NEW.habit_id AND NEW.completion_date < created_date)
BEGIN
    SELECT RAISE(ABORT, 'completion date precedes habit creation');
END;

CREATE TRIGGER completions_check_start_update
BEFORE UPDATE OF habit_id, completion_date ON completions
WHEN EXISTS (SELECT 1 FROM habits WHERE habit_id = NEW.habit_id AND NEW.completion_date < created_date)
BEGIN
    SELECT RAISE(ABORT, 'completion date precedes habit creation');
END;

CREATE TRIGGER habits_created_date_immutable
BEFORE UPDATE OF created_date ON habits
WHEN NEW.created_date <> OLD.created_date
BEGIN
    SELECT RAISE(ABORT, 'created_date is immutable');
END;
