from flask import Flask, request, render_template, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('meteo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS dati (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    temperature REAL,
                    humidity REAL,
                    pressure REAL,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dati', methods=['POST'])
def ricevi_dati():
    data = request.get_json()
    try:
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        pressure = float(data['pressure'])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect('meteo.db')
        c = conn.cursor()
        c.execute("INSERT INTO dati (temperature, humidity, pressure, timestamp) VALUES (?, ?, ?, ?)",
                  (temperature, humidity, pressure, timestamp))
        conn.commit()
        conn.close()
        return {"message": "Dati salvati con successo."}, 200
    except Exception as e:
        return {"error": str(e)}, 400

@app.route('/api/dati')
def api_dati():
    conn = sqlite3.connect('meteo.db')
    c = conn.cursor()
    c.execute("SELECT temperature, humidity, pressure, timestamp FROM dati ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()

    rows.reverse()
    return jsonify({
        'labels': [row[3] for row in rows],
        'temperatures': [row[0] for row in rows],
        'humidities': [row[1] for row in rows],
        'pressures': [row[2] for row in rows]
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
