from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.sqlite'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    name = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(20), nullable=False, unique=False)

class Chatroom(db.Model):
    __tablename__ = "chatroom"

    name = db.Column(db.String(80), primary_key=True)
    messages = db.relationship('Message', backref='Chatroom',lazy=True)

    def add_message(self,username, message):
        new = Message(user = username, message = message, chatroom = self.name)
        db.session.add(new)
        db.session.commit()


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80),nullable=False)
    message = db.Column(db.String(256),nullable=False)
    chatroom = db.Column(db.String(80),db.ForeignKey('chatroom.name'),nullable=False)


if __name__ == "__main__":
    db.create_all()