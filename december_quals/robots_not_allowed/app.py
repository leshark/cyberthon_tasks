from hashlib import md5

from flask import Flask, send_from_directory, request, abort, render_template

app = Flask(__name__, static_folder='static')

FLAG = "CYBERTHON{ya_dolzen_tancevat}"

urls = {md5(str(key).encode()).hexdigest(): "nothing here, go away" for key in range(1, 100)}
urls["03afdbd66e7929b125f8597834fa83a4"] = FLAG


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/<path:other_url>')
def fallback(other_url):
    if urls.get(other_url):
        return urls[other_url]
    abort(404)
