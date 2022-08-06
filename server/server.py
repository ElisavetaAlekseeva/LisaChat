from flask import Flask, request
from nbformat import from_dict
import core as core

def register_user(login, pas):
    return f'User {login} successfully added!'

app = Flask(__name__)

@app.route("/api", methods=['GET'])
def home():
    return "<h1> Hello World! </h1>"

@app.route("/register", methods=['POST'])
def register():
    return core.register_user(request.json)

@app.route("/delete", methods=['POST'])
def delete():
    print (request.json)
    return core.delete_user(request.json)

@app.route("/api/chat", methods=['GET'])
def getChatById():
    if 'id' in request.args:
        id = request.args['id']
    if 'user' in request.args:
        user = request.args['user']
    if 'addr' in request.args:
        addr = request.args['addr']
    return f"<h1> ChatId: {id} message from {user} to {addr}<h2>"

@app.route("/login", methods=['GET'])
def login():
    if 'login' in request.args:
        login = request.args['login']
    if 'password' in request.args:
        password = request.args['password']
    return core.login_user(login,password)
    
@app.route("/contacts",methods=['GET'])
def contacts():
    if 'id' in request.args:
        id = request.args['id']
    return core.get_contacts(id)

@app.route("/info", methods=['GET'])
def get_user_info():
    if 'id' in request.args:
        user_id = request.args['id']
        return core.user_info(user_id)
    
@app.route("/name", methods=['GET'])
def get_user_name():
    if 'id' in request.args:
        user_id = request.args['id']
        return core.user_name(user_id)

@app.route("/chatwith", methods=['GET'])
def open_chat():
    if 'id' in request.args:
        user_id = request.args['id']
        return core.get_chat(user_id)

@app.route("/getChatId", methods=['GET'])
def get_chat_id():
    if ('from' in request.args) and ('to' in request.args):
        from_id = request.args['from']
        to_id = request.args['to']
        return core.get_chat_id(from_id, to_id)

@app.route("/sendMessage",methods=['POST'])
def send_message():
    return core.send_message(request.json)


@app.route("/getMessages", methods=['GET'])
def get_messages():
    if 'chat_id' in request.args:
        chat_id = request.args['chat_id']
    if 'user_id' in request.args:
        user_id = request.args['user_id'] 
    return core.get_messages(chat_id,user_id)

@app.route("/getLastUpdate", methods=['GET'])
def get_last_update():
    if 'chat_id' in request.args:
        chat_id = request.args['chat_id']
    if 'user_id'in request.args:
        user_id = request.args['user_id']
    return core.get_last_update(chat_id,user_id)

app.run()
