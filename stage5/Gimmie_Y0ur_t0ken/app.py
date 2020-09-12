import os

from flask import Flask, request, render_template, redirect, url_for, abort, escape
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import login_user, current_user, LoginManager
from flask_login import UserMixin
import jwt

from send_email import send_email
from utils import url_serializer

root_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET"].encode()
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(root_dir, 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'user_avatars')
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    avatar = db.Column(db.String(80))
    email_confirmed = db.Column(db.Boolean, default=False)
    _password = db.Column(db.String(128))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = generate_password_hash(plaintext)

    def has_correct_password(self, plaintext):
        return check_password_hash(self._password, plaintext)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db.create_all()


# ensure we always have admin
admin = User(username='admin', email='admin1234@example.com', password="lolkek3210", avatar="avatar_base.png")
db.session.add(admin)
db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template("index.html", username=escape(current_user.username),
                               flag="CYBERTHON{4eck_Y0u3_JWT_T0kens}" if current_user.username == "admin" else "flag only for admin")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("login", "")
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user is not None and user.has_correct_password(password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Wrong username or password. Try again")
    return render_template("login.html")


# noinspection PyArgumentList
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        link_to_img = os.path.join("static", "assets", "img", "avatar_base.png")

        if User.query.filter_by(username=username).first() is not None:
            return render_template("registration.html", error="User with such username already exists")
        elif User.query.filter_by(email=email).first() is not None:
            return render_template("registration.html", error="User with such email already exists")

        reg = User(username=username, email=email, password=password, avatar=link_to_img)
        db.session.add(reg)
        db.session.commit()

        email_token = url_serializer.dumps(reg.username)
        confirm_url = url_for('confirm_email', token=email_token, _external=True)
        html = render_template('activate_mail.html', confirm_url=confirm_url)

        send_email(email, 'Confirm your email', html)

        return redirect(url_for("login"))
    return render_template("registration.html")


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        username = url_serializer.loads(token).get("username", "")
        user = User.query.filter_by(username=username).first_or_404()

        user.email_confirmed = True
        db.session.commit()
    except jwt.InvalidTokenError as e:
        abort(401, description=f"{e}")

    return redirect(url_for('login'))


@app.route('/reset', methods=["GET", "POST"])
def reset():
    if request.method == "POST":
        email = request.form.get('email', '')

        user = User.query.filter_by(email=email).first()

        if user is None:
            return render_template("reset_password.html", error="User with such email does not exist")
        if not user.email_confirmed:
            return render_template("reset_password.html", error="You need to confirm your email first")

        email_token = url_serializer.dumps(user.username)
        recover_url = url_for('reset_with_token', token=email_token, _external=True)
        html = render_template('recover.html', confirm_url=recover_url)
        send_email(email, 'Account auth link required', html)

        return redirect(url_for('login'))
    return render_template('reset_password.html')


@app.route('/reset/<token>', methods=["GET"])
def reset_with_token(token):
    try:
        username = url_serializer.loads(token).get("username", "")
    except jwt.InvalidTokenError as e:
        abort(401, description=f"{e}")

    user = User.query.filter_by(username=username).first_or_404()
    login_user(user)

    return render_template("index.html", username=escape(current_user.username),
                           flag="CYBERTHON{4eck_Y0u3_JWT_T0kens}" if current_user.username == "admin" else "flag only for admin")
