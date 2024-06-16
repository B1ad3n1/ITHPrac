from flask import Flask, request, jsonify
import configparser
import mysql.connector

app = Flask(__name__)

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
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except mysql.connector.Error as err:
        return {'error': str(err)}

@app.route('/logs', methods=['GET'])
def get_logs():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    ip = request.args.get('ip')

    query = "SELECT * FROM logs WHERE timestamp BETWEEN %s AND %s"
    params = [start_date, end_date]

    if ip:
        query += " AND ip = %s"
        params.append(ip)

    logs = execute_query(query, params)
    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)