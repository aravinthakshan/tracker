
from flask import Flask, render_template, jsonify
import csv
import os

app = Flask(__name__)
LOG_FILE = "logs/usage_log.csv"

def read_log():
    if not os.path.isfile(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as file:
        reader = csv.DictReader(file)
        return list(reader)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    logs = read_log()
    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True)
