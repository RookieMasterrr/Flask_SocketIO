from logging import debug
from flask import Flask,render_template
from flask.globals import request
from flask_socketio import SocketIO, emit, join_room, leave_room, send

app=Flask(__name__)
app.config["SECRET_KEY"]="SECRET"
socketio = SocketIO(app,async_mode = 'eventlet')

user_room_dict={}
sid_user_dict={}

@socketio.on('message')
def handle_message(msg):
    print(request.sid)
    emit("message",msg,broadcast=True)

@socketio.on('join')
def join_a_room(data):
    print(data)
    roomid=data["room"]
    join_room(roomid)

    user_room_dict[request.sid]=roomid

    emit("Roommessage",sid_user_dict[request.sid]+" enter the room",to=roomid)

@socketio.on('leave')
def leave_a_room(data):
    print(data)
    roomid=data["room"]
    leave_room(roomid)

    emit("Roommessage",sid_user_dict[request.sid]+" leave the room",to=roomid)

    del user_room_dict[request.sid]



@socketio.on('toSomeRoom')
def toSomeRoom(Msg):
    roomid=user_room_dict[request.sid]
    emit('Roommessage',sid_user_dict[request.sid]+":"+Msg,to=roomid)

@socketio.on('changeName')
def changeName(name):
    sid_user_dict[request.sid]=name


@app.route('/')
def index():
    return render_template('broadcast_page.html')

if __name__=="__main__":
    socketio.run(app,debug=1)