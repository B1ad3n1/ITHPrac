import argparse
import configparser
import mysql.connector
from datetime import datetime

# Чтение конфигурационного файла
config = configparser.ConfigParser()
config.read('config.ini')

db_config = {
    'user': config['DEFAULT']['db_user'],
    'password': config['DEFAULT']['db_password'],
    'host': config['DEFAULT']['db_host'],
    'database': config['DEFAULT']['db_name']
}

def execute_query(query, params=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

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

def view_logs_by_date(date):
    query = "SELECT * FROM logs WHERE DATE(timestamp) = %s"
    logs = execute_query(query, (date,))
    for log in logs:
        print(log)

def view_logs_by_date_and_ip(date):
    query = "SELECT ip, COUNT(*) as request_count FROM logs WHERE DATE(timestamp) = %s GROUP BY ip"
    logs = execute_query(query, (date,))
    for log in logs:
        print(log)

def view_logs_by_date_ip_status(date):
    query = "SELECT ip, status, COUNT(*) as request_count FROM logs WHERE DATE(timestamp) = %s GROUP BY ip, status"
    logs = execute_query(query, (date,))
    for log in logs:
        print(log)

def view_logs_by_date_range(start_date, end_date):
    query = "SELECT * FROM logs WHERE timestamp BETWEEN %s AND %s"
    logs = execute_query(query, (start_date, end_date))
    for log in logs:
        print(log)

def view_logs_by_date_range_and_ip(start_date, end_date):
    query = "SELECT ip, COUNT(*) as request_count FROM logs WHERE timestamp BETWEEN %s AND %s GROUP BY ip"
    logs = execute_query(query, (start_date, end_date))
    for log in logs:
        print(log)

def main():
    parser = argparse.ArgumentParser(description="Logwriter - A tool for parsing and viewing Apache logs")
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for 'parse' command
    subparsers.add_parser('parse', help='Parse log files and save to database')

    # Subparser for 'view' command
    view_parser = subparsers.add_parser('view', help='View logs')
    view_parser.add_argument('start_date', help='Start date in DD.MM.YYYY format')
    view_parser.add_argument('end_date', nargs='?', help='End date in DD.MM.YYYY format')
    view_parser.add_argument('filters', nargs='*', help='Filters: ip, status')

    args = parser.parse_args()

    if args.command == 'parse':
        parse_logs()
    elif args.command == 'view':
        start_date = datetime.strptime(args.start_date, '%d.%m.%Y').strftime('%Y-%m-%d')
        if args.end_date:
            end_date = datetime.strptime(args.end_date, '%d.%m.%Y').strftime('%Y-%m-%d')
            if 'ip' in args.filters:
                view_logs_by_date_range_and_ip(start_date, end_date)
            else:
                view_logs_by_date_range(start_date, end_date)
        else:
            if 'ip' in args.filters:
                if 'status' in args.filters:
                    view_logs_by_date_ip_status(start_date)
                else:
                    view_logs_by_date_and_ip(start_date)
            else:
                view_logs_by_date(start_date)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()