from flask import Flask, request, render_template, session
from uuid import uuid4

import os

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET"].encode()


@app.route('/')
def hello_world():
    old_passw = str(uuid4())[:16]
    session["old_password"] = old_passw
    return render_template("index.html", password=old_passw)


@app.route('/change_passw', methods=["POST"])
def change_passw():
    new_passw = str(uuid4())[:16]
    session["new_password"] = new_passw
    return new_passw


@app.route('/check', methods=["POST"])
def check_passw():
    if not session.get("old_password"):
        return "I don't remember you. 私のza pazwardoレクイエムの力を超えることはできません。 すべてのアクションはゼロに戻ります！"
    if request.form.get("new_passw", "F") == session["old_password"]:
        return "CYBERTON{w0w_y0u_kn0w_ja8asc3ipt}"
    session["old_password"] = session["new_password"]
    return request.json["new_passw"]
