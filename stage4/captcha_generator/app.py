import hashlib

from flask import Flask, request, render_template, session
import json
import os

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET"].encode()

# total amount of captcha
CAPTCHA_NUM = 400


def check_answer(level, user_answer):
    with open("answers.json", "r") as f:
        answers = json.load(f)
        return answers[str(level)] == user_answer


def get_captcha_name():
    return hashlib.md5(f"captcha{session['level']}".encode()).hexdigest() + ".png"


@app.route('/')
def hello_world():
    if not session.get("level"):
        session["level"] = 0
    elif session["level"] == CAPTCHA_NUM - 1:
        return render_template("index.html", image="final.png", error="CYBERTHON{supe3_345y_0cr}")
    return render_template("index.html", image=get_captcha_name())


@app.route('/check', methods=["POST"])
def check():
    if not session.get("level"):
        session["level"] = 0
    num = request.form.get("example", "f")
    try:
        num = int(num)
        if session["level"] == CAPTCHA_NUM - 1:
            return render_template("index.html", image="final.png", error="CYBERTHON{supe3_345y_0cr}")
        if check_answer(session["level"], num):
            session["level"] += 1
            return render_template("index.html", image=get_captcha_name(), error=f"Solved {session['level']} of {CAPTCHA_NUM}")
    except ValueError as e:
        print(e)
    return render_template("index.html", error="Incorrect solution. try again", image=get_captcha_name())

