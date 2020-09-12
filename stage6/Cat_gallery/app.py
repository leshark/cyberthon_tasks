import os

from flask import Flask, request, send_file, render_template, send_from_directory

app = Flask(__name__, static_folder='static')


# if you see this you are in the right way

def is_safe_path(path):
    return os.path.realpath(path).startswith(os.getcwd()) or os.path.realpath(path).startswith(
        os.path.join(os.getcwd(), "static"))


@app.route('/')
def index():
    image_name = request.args.get('image_name')
    if not image_name:
        return render_template("index.html")
    if is_safe_path(os.path.join(os.getcwd(), "static", image_name)):
        return send_file(os.path.join(os.getcwd(), "static", image_name))
    else:
        return "Hacking attempt discovered. Viewing files upper than application directory is not permitted. This " \
               "incident will be reported. "


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

