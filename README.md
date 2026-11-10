# Лабораторная работа № 4: трекер полезных привычек

Лазарев Александр Евгеньевич · ОИСТ-412

Проектирование SQLite-схемы для MVP группового проекта. Подготовлены ER-диаграмма, DDL, тестовые данные, обоснование 3NF и автоматические проверки. Это учебная модель, а не подключённая к приложению база.

- [ER-диаграмма SVG](docs/database/er_diagram.svg) и [PNG](docs/database/er_diagram.png)
- [Схема и ограничения](database/schema.sql)
- [Тестовые данные](database/seed_data.sql)
- [Нормализация для Wiki](database/normalization.md)
- [Тесты схемы](tests/test_schema.py)

Проверить локально из этой папки:

```sh
python3 -m unittest discover -s tests -v
```

Для новой SQLite-базы:

```sh
sqlite3 habits.db < database/schema.sql
sqlite3 habits.db < database/seed_data.sql
```

Перед операциями с базой приложение должно включать `PRAGMA foreign_keys = ON` на каждом подключении. Локальная дата пользователя и запрет будущих отметок проверяются приложением. Применять скрипты к существующей базе без отдельного плана миграции нельзя. Модель аккаунтов и синхронизации ещё не согласована.

Материалы подготовлены для публичного репозитория [habit-tracker-lab4](https://github.com/scorpochabro-solo/habit-tracker-lab4). Процесс нормализации также представлен в Wiki проекта.
