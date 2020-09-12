from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/check_time', methods=["POST"])
def check_time():
    time = request.json.get("t", "F")
    try:
        year = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ").year
        if year == 2045:
            return "CYBERTON{t1me_t3avell1ng}"
    except ValueError:
        pass
    return "singularity has not yet arrived"
