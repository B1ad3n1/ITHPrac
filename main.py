import sys
from db import session, LogEntry
from log_parser import parse_logs
from datetime import datetime

def view_logs(start_date=None, end_date=None, ip=None):
    query = session.query(LogEntry)

    if start_date:
        query = query.filter(LogEntry.timestamp >= start_date)
    if end_date:
        query = query.filter(LogEntry.timestamp <= end_date)
    if ip:
        query = query.filter(LogEntry.ip == ip)

    logs = query.all()
    for log in logs:
        print(log.__dict__)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == 'parse':
        parse_logs()
    elif len(sys.argv) >= 2:
        start_date = None
        end_date = None
        ip = None

        if len(sys.argv) >= 2:
            start_date = datetime.strptime(sys.argv[1], '%d.%m.%Y')
        if len(sys.argv) >= 3:
            end_date = datetime.strptime(sys.argv[2], '%d.%m.%Y')
        if len(sys.argv) >= 4:
            ip = sys.argv[3]
