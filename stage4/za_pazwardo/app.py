from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/check')
def check_passw():
    if request.args.get('password', 'F') == "24msecb785falqdss":
        return "CYBERTHON{b3ute_fo3ce_p0we3}"
    return render_template("index.html", error="Incorrect password")
