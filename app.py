from flask import Flask, request, redirect, render_template, session
from flask_socketio import SocketIO
from string import ascii_uppercase
import random



app = Flask(__name__)
# app.config["SECRET_KEY"] = ""
socketio = SocketIO(app)

rooms = {}

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        join = request.form.get('join')
        create = request.form.get('create')

        #it means person is joining a room:
        if join:
            pass
        #it means person is creating a room:
        if create:
            generated_code = generate_room_code(4)
            print(generated_code)
            rooms[generated_code] = {'members':0, 'messages':[]}
            session['room'] = generated_code
            session['name'] = name



    return render_template('home.html')


def generate_room_code(length):
    while True:
        code = ""
        for _ in length:
            code = code + random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code

if __name__ == '__main__':
    socketio.run(app)