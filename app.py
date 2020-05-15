from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
from models import *
from flask_session import Session
from sqlalchemy import and_
import requests
import os
from flask_socketio import SocketIO, emit


#key
# key = "UVD8w0gOPRawwpiWg6WDA"
# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret'
app.config['DEBUG'] = True
socketio = SocketIO(app)
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# Session(app)

@app.route("/")
def index():
    '''
    Home page
    '''
    session['user'] = None
    return render_template("home.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html", text = "Sign me up!", url = "sign_up_result",error_text="")

@app.route("/sign_in")
def sign_in():
    return render_template("sign_up.html",text = "Sign me in!", url = "sign_in_result",error_text="")


@app.route("/sign_up_result", methods = ["POST"])
def sign_up_result():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username)
    to_add = User(name=username,password=password)
    check = User.query.get(username)
    if check:
        return render_template("sign_up.html",text = "Sign me up!", url = "sign_in_result",error_text="username already taken")
    else:
        session['user'] = username
        db.session.add(to_add)
        db.session.commit()
        chatrooms = Chatroom.query.all()
        return redirect(url_for("chat", chatroom = None, rooms = chatrooms))

    

@app.route("/sign_in_result", methods = ["POST"])
def sign_in_result():
    username = request.form.get("username")
    password = request.form.get("password")
    check = User.query.get(username)
    if not check:
        return render_template("sign_up.html",text = "Sign me in!", url = "sign_in_result",error_text="no such username")
    else:
        if password == check.password:
            session["user"]=username
            chatrooms = Chatroom.query.all()
            return redirect(url_for("chat", chatroom = None, rooms = chatrooms))
        else:
            return render_template("sign_up.html",text = "Sign me in!", url = "sign_in_result",error_text="wrong password")

@app.route("/chat")
def chat():
    chatroom = request.args.get("chatroom")
    chatrooms = Chatroom.query.all()
    if chatroom == None :
        return render_template("chatroom.html", messages = [], rooms = chatrooms, theroom = None)
    else:
        room = Chatroom.query.get(chatroom)
        print(chatroom)
        messages = room.messages
        for message in messages:
            print(message)
        return render_template("chatroom.html", messages = messages, rooms = chatrooms, theroom = room)

@app.route("/create_room" ,methods = ["GET","POST"])
def create_room():
    if request.method == 'GET':
        return render_template("create_room.html")
    else:
        name = request.form.get("name")
        to_add = Chatroom(name = name)
        to_check = Chatroom.query.get(name)
        if to_check!=None:
            return render_template("create_room.html", error_code="please give a unique name")
        else:
            db.session.add(to_add)
            db.session.commit()
            chatrooms = Chatroom.query.all()
            room = Chatroom.query.get(name)
            messages = room.messages
            return render_template("chatroom.html", messages = messages, rooms = chatrooms, theroom = room)

@socketio.on("send message")
def send_message(data):
    message = data['message']
    user = session["user"]
    room = data['room']
    print(message)
    print(user)
    print(room)
    chatroom = Chatroom.query.get(room)
    chatroom.add_message(username = user, message = message)
    emit('tell message' ,{ 'user' : user , 'message' : message}, broadcast = True)
