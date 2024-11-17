from flask import Flask, request, redirect, render_template, session
from flask_socketio import SocketIO



app = Flask(__name__)
# app.config["SECRET_KEY"] = ""
socketio = SocketIO(app)


@app.route('/', ["POST", "GET"])
def home():
    return render_template('home.html')