# Log Aggregator

## Описание

Приложение для агрегирования данных из access логов веб-сервера Apache с сохранением в базу данных MySQL и возможностью просмотра данных через консоль и API.

## Установка

1. Установите необходимые зависимости:
    ```bash
    pip install -r requirements.txt
    ```

2. Настройте файл `config.ini`:
    ```ini
    [DEFAULT]
    files_dir = C:/Apache24/logs
    ext = log
    format = %h %l %t "%r" %>s %b
    db_user = log_user
    db_password = password
    db_host = localhost
    db_name = log_aggregator
    ```

3. Создайте базу данных и таблицы:
    ```sql
    CREATE DATABASE log_aggregator;
    USE log_aggregator;
    CREATE TABLE logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ip VARCHAR(15),
        timestamp DATETIME,
        request TEXT,
        status INT,
        size INT
    );
    ```

## Использование

### Парсинг логов

Запуск парсера вручную:
```bash
python logwriter.py parse