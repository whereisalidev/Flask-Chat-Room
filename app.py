from flask import Flask, request, redirect, render_template, session
from flask_socketio import SocketIO



app = Flask(__name__)
# app.config["SECRET_KEY"] = ""
socketio = SocketIO(app)



@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        


    return render_template('home.html')


if __name__ == '__main__':
    socketio.run(app)