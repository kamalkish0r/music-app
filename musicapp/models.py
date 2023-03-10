import jwt
from time import time
from flask_login import UserMixin
from flask import current_app as app
from musicapp import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    songs = db.relationship('Song', backref='owner', lazy=True)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"

    def get_reset_token(self, expires_sec=1800):
        return jwt.encode({'user_id': self.id, 'exp': time() + expires_sec}, key=app.config['SECRET_KEY'])

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=['HS256'])[
                'user_id']
        except:
            return None
        return User.query.get(user_id)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    artist = db.Column(db.String(50), nullable=False)
    album = db.Column(db.String(50))
    filename = db.Column(db.String(150), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Song('{self.title}', '{self.artist}', '{self.album}', '{self.filename}', '{self.owner_id}')"
