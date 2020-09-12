import os

from flask import Flask, request, render_template, render_template_string, send_from_directory, session, redirect, \
    url_for

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ["FLASK_SECRET"].encode()
app.config["SECRET_DATA"] = "CYBERTHON{se3ve3_s1de_temp1ate_1njec6ion}"

allowed_ext = [".jpg", ".png", ".gif"]
blocked_chars = ["\"", "'", "[", "]", "_"]


def is_safe_path(path):
    return os.path.realpath(path).startswith(os.getcwd()) or os.path.realpath(path).startswith(
        os.path.join(os.getcwd(), "static"))


def validate(passw):
    return all([char not in passw for char in blocked_chars])


@app.route('/')
def index():
    if "username" in session:
        # let's pretend all html is processed with render_template_string
        if validate(session["username"][0]):
            user = render_template_string(session["username"][0])
        else:
            user = "Not this time"
    else:
        user = None

    cat_type = request.args.get('cat_type')
    if not cat_type:
        return render_template("index.html", username=user)

    cat_dir = os.path.join("static", cat_type)
    if is_safe_path(cat_dir):
        return render_template("index.html", username=user,
                               imgs=[os.path.join(cat_dir, file) for file in os.listdir(cat_dir) if
                                     file[-4:] in allowed_ext])
    else:
        return "Hacking attempt discovered. Viewing files upper than application directory is not permitted. This " \
               "incident will be reported. "


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if 'username' not in session:
            return render_template("sign_in.html", error="no user with such username exists!")
        elif session['username'][1] != password:
            return render_template("sign_in.html", error="wrong password!")
        return redirect(url_for("index"))

    return render_template("sign_in.html")


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if validate(username):
            session['username'] = (username, password)
            return redirect("sign_in")
        else:
            return render_template("sign_up.html", error="Username contains invalid characters!")

    return render_template("sign_up.html")


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
