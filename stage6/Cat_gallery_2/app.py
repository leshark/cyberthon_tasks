import os

from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__, static_folder='static')


def is_safe_path(path):
    return os.path.realpath(path).startswith(os.getcwd()) or os.path.realpath(path).startswith(
        os.path.join(os.getcwd(), "static"))


@app.route('/')
def index():
    cat_type = request.args.get('cat_type')
    if not cat_type:
        return render_template("index.html")

    cat_dir = os.path.join("static", cat_type)
    if is_safe_path(cat_dir):
        return render_template("index.html", imgs=[os.path.join(cat_dir, file) for file in os.listdir(cat_dir)])
    else:
        return "Hacking attempt discovered. Viewing files upper than application directory is not permitted. This " \
               "incident will be reported. "


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

