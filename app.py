from flask import Flask, render_template, jsonify
import csv
import os
from collections import Counter

app = Flask(__name__)
LOG_FILE = "logs/usage_log.csv"

def read_log():
    if not os.path.isfile(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as file:
        reader = csv.DictReader(file)
        return list(reader)

def get_time_distribution():
    logs = read_log()
    counter = Counter([log["Category"] for log in logs if log["Status"] == "Active"])
    return counter

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    logs = read_log()
    return jsonify(logs)

@app.route("/time_distribution")
def time_distribution():
    distribution = get_time_distribution()
    return jsonify(distribution)

if __name__ == "__main__":
    app.run(debug=True)
