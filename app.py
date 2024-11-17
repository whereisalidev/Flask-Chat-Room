from flask import Flask, request, redirect, render_template, session
from flask_socketio import SocketIO



app = Flask(__name__)
socketio = SocketIO(app)

