from flask import Flask, request

app = Flask(__name__)

FLAG = "CYBERTHON{Cu3t0m_exT3nSi0n}"

TRUE_SONG = '''Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you'''


@app.route('/')
def check_song():
    headers = request.headers
    song = []
    song.append(headers.get("S1", "lol"))
    song.append(headers.get("S2", "lol"))
    song.append(headers.get("S3", "lol"))
    song.append(headers.get("S4", "lol"))
    song.append(headers.get("S5", "lol"))
    song.append(headers.get("S6", "lol"))
    if song == TRUE_SONG.split("\n"):
        return FLAG
    else:
        return "you're too blind to see"
