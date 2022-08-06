import db

def register_user(data):
    try:
        login, pswd = data.values()
        return db.create_user(login, pswd)
    except:
        return 'Error on register'

def delete_user(data):
    try:
        return db.delete_user(data['id'])
    except:
        return 'Error on delete'

def login_user(login, password):
    try:
        return str(db.user_login(login,password))
    except:
        return 'Error on login'


def get_contacts(user_id):
    try:
        return db.get_user_contacts(user_id)
    except:
        return 'Error on get_contacts'

def user_info(user_id):
    try:
        return db.get_user_info(user_id)
    except:
        return 'Error on get_info'

def user_name(user_id):
    try:
        return db.get_name(user_id)
    except:
        return 'Error on user_name'


def get_chat_id(from_id, to_id):
    try:
        if db.get_chat_id(from_id, to_id):
            return  db.get_chat_id(from_id, to_id)
        else:
            db.create_chat(from_id, to_id)
            return db.get_chat_id(from_id, to_id)
    except:
        return 'Error on get_chat_id'


def send_message(data):
    try:
        chat_id, from_id, text = data.values()
        return db.send_message(chat_id, from_id, text)
    except:
        return 'Error on create_message'


def get_messages(chat_id,user_id):
    try:
        return db.get_messages(chat_id,user_id)
    except:
        return 'Error on get_messages'

def get_last_update(chat_id,user_id):
    try:
        return db.get_last_update(chat_id,user_id)
    except:
        return 'Error on get_last_update'
