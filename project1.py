import os
import json
import flask
from flask.templating import render_template
from flask_wtf.recaptcha import validators
from werkzeug.utils import redirect
from wtforms.fields.simple import SubmitField
import getData
from flask_sqlalchemy import SQLAlchemy
import accessories
import flask_login
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError


app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SECRET_KEY"] = os.getenv("SKEY")


db = SQLAlchemy(app)


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL").replace(
    "://", "ql://", 1
)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Maintaining a session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User database table creation
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)


# Registration validation
class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=2, max=63)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=2, max=63)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("Username already exists, choose a different one")


# Login validation and storage
class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=2, max=63)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=2, max=63)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Login")


# Artists database table creation
class artists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    artist_id = db.Column(db.String(120), nullable=False)
    artist_name = db.Column(db.String(120))


db.create_all()


# Global vars
song_name = ""
artist_name = ""


# Login page, from landing page
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if form.password.data == user.password:
                login_user(user)
                return flask.redirect(flask.url_for("profile"))
            else:
                flask.flash("Invalid password")
        else:
            return flask.redirect(flask.url_for("invalid"))

    return flask.render_template("login.html", form=form)


@app.route("/invalid")
def invalid():
    return flask.render_template("invalid.html")


# Logout page, redirects to login prompt
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for("login"))


# Registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            new_user = User(username=form.username.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return flask.redirect(flask.url_for("login"))
        else:
            flask.flash("Username already exists")

    return flask.render_template("register.html", form=form)


# User profile page
@app.route("/profile", methods=["GET", "POST"])
def profile():
    artist_list = artists.query.filter_by(
        username=flask_login.current_user.username
    ).all()
    artist_IDs = []
    artist_names = []

    for artist in artist_list:
        artist_IDs.append(artist.artist_id)
        artist_names.append(artist.artist_name)

    if flask.request.method == "POST":
        if flask.request.form.get("artist_ID") == "":
            print("Emtpy entry")
            pass
        else:
            validator = accessories.check_valid_id(flask.request.form.get("artist_ID"))
            if flask.request.form.get("artist_ID") not in artist_IDs and validator[0]:
                artist = artists(
                    username=flask_login.current_user.username,
                    artist_id=flask.request.form.get("artist_ID"),
                    artist_name=validator[1],
                )
                db.session.add(artist)
                db.session.commit()
                artist_IDs.append(artist.artist_id)
                artist_names.append(artist.artist_name)
            else:
                flask.flash("Artist is invalid or already exists")

    return flask.render_template(
        "profile.html",
        usern=flask_login.current_user.username,
        artists_list=artist_names,
        len=len(artist_names),
    )


# Landing page re-route
@app.route("/")
def goToLogin():
    return flask.redirect(flask.url_for("login"))


# Main page
@app.route("/homepage", methods=["GET", "POST"])
@login_required
def index():
    global song_name
    global artist_name
    previewExists = {}

    # Authenticaion for spotify API
    try:
        artist_list = artists.query.filter_by(
            username=flask_login.current_user.username
        ).all()
        artist_IDs = []

        for artist in artist_list:
            artist_IDs.append(artist.artist_id)

        token = getData.getAuthToken()
        dataList = getData.getSongs(token, artist_IDs)

        if type(dataList["Preview"] == "NoneType"):
            previewExists["Preview"] = "No preview available"
        else:
            previewExists["Preview"] = ""

        song_name = dataList["Song"]
        artist_name = dataList["Artist"]
    except:
        token = "/static/Error_Message.png"
        dataL = []
        dataL.append(
            {
                "Song": "Unavailable",
                "Artist": "Error",
                "Image": "/static/Error_Message_empty.png",
                "Preview": "Unavailable",
            }
        )
        previewExists["Preview"] = "No preview available"
        dataList = dataL[0]

    print(dataList)

    return flask.render_template(
        "index.html", len=len(dataList), dataList=dataList, previewExists=previewExists
    )


# Lyrics page
@app.route("/lyrics")
def lyricsPage():
    global artist_name
    global song_name

    # Get genius authentication and return the lyrics
    lyricsObject = getData.getGeniusAuth(song_name, artist_name)
    list_lyrics = lyricsObject.split("/n")

    # Check if lyrics object is a proper string, if not then there are no lyrics present in the genius page
    if isinstance(list_lyrics[0][0], int):
        list_lyrics = "No lyrics available"

    if song_name == "Unavailable":
        list_lyrics = "Unavailable"

    return flask.render_template(
        "lyricsPage.html", len=len(list_lyrics), lyrics=list_lyrics
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)), debug=True)
