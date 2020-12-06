import os

from flask import Flask, redirect, send_from_directory, render_template

app = Flask(__name__, static_folder='static')

FLAG = [
    "C", "Y", "B", "E", "R", "T", "H", "O", "N", "{", "t00_", "mAnY_", "3ed13ect7", "}"
]

ROUTES = {FLAG[key]: FLAG[key + 1] for key in range(len(FLAG) - 1)}


@app.route("/")
def hello():
    return redirect("/C")


@app.route("/}")
def end():
    return render_template("index.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/<letter>')
def go_next_page(letter):
    return redirect("/" + ROUTES[letter])
