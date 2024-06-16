import os
import configparser
from datetime import datetime
import mysql.connector

# Чтение конфигурационного файла
config = configparser.ConfigParser()
config.read('config.ini')

db_config = {
    'user': config['DEFAULT']['db_user'],
    'password': config['DEFAULT']['db_password'],
    'host': config['DEFAULT']['db_host'],
    'database': config['DEFAULT']['db_name']
}

def parse_log_line(line):
    parts = line.split()
    ip = parts[0]
    timestamp_str = parts[3][1:]  # Удаляем [
    timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S')
    request = parts[5][1:] + ' ' + parts[6] + ' ' + parts[7][:-1]  # Удаляем " с обеих сторон
    status = int(parts[8])
    size = int(parts[9]) if parts[9].isdigit() else 0
    return ip, timestamp, request, status, size

def save_to_db(entries):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO logs (ip, timestamp, request, status, size) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(query, entries)
    conn.commit()
    cursor.close()
    conn.close()

def parse_logs():
    log_dir = config['DEFAULT']['files_dir']
    log_ext = config['DEFAULT']['ext']
    entries = []

    if not os.path.exists(log_dir):
        raise FileNotFoundError(f"Directory {log_dir} does not exist.")

    for filename in os.listdir(log_dir):
        if filename.endswith(log_ext):
            with open(os.path.join(log_dir, filename)) as f:
                for line in f:
                    entries.append(parse_log_line(line))

    save_to_db(entries)

if __name__ == "__main__":
    parse_logs()