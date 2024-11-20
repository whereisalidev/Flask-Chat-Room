from flask import Flask, request, redirect, render_template, session, url_for
from flask_socketio import SocketIO, send, join_room, leave_room
from string import ascii_uppercase
import random



app = Flask(__name__)
app.config["SECRET_KEY"] = "JustFormality_otherwise_it_gives_error"
socketio = SocketIO(app)

rooms = {}

@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        join = request.form.get('join', False)
        create = request.form.get('create', False)

        #it means person is creating a room:
        if create != False:
            generated_code = generate_room_code(4)
            rooms[generated_code] = {'members':0, 'messages':[]}
            session['room'] = generated_code
            session['name'] = name
            return redirect(url_for('room'))
        
        #it means person is joining a room, then first check if the given code room exists or not?:
        elif code not in rooms:
            print('Room does not exist.')
            return render_template('home.html', error='Room does not exist', name=name, code=code)

        elif join != False:
            #assign the session with name room to given code and go to room page
            session['room'] = code
            session['name'] = name
            return redirect(url_for('room'))

    return render_template('home.html')



@app.route('/room')
def room():
    room = session.get('room')
    if room is None or session.get('name') is None or room not in rooms:
        return redirect(url_for('home'))

    return render_template('room.html', code=room, messages=rooms[room]['messages'])



@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")



@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")



@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")



def generate_room_code(length):
    while True:
        code = ""
        for _ in range(length):
            code = code + random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)