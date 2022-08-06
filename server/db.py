import psycopg2

try:
    connection = psycopg2.connect(user="elisaveta",
                                  password="pg2022Lisa",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="LisaChat")
    cursor = connection.cursor()

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

def get_user_info(user_id):
    try:
        cursor.execute(f"SELECT * FROM info where user_id = {user_id}")
        fetch = cursor.fetchall()
        row_list_keys = ['id', 'name']
        row_list_val = [item for t in fetch for item in t]
        row_dict = dict(zip(row_list_keys,row_list_val))
        return row_dict
    except:
        return None

def user_login(name, pswd):
    try:
        cursor.execute(f"SELECT user_id FROM info where name = '{name}' and password = '{pswd}'")
        fetch = cursor.fetchall()[0][0]
        return fetch
    except:
        return None


def create_user(user_id, pswd):
    try:
        cursor.execute(f"""insert into info 
                        values 
                        (default,'{user_id}','{pswd}')""")
        connection.commit()
        return f'User {user_id} successfully created!'
    except:
        return None

def delete_user(id):
    try:
        cursor.execute(f"""delete from info 
                        where user_id = {id}""")
        connection.commit()
        return 'User successfully deleted!'
    except:
        return None


def create_chat(from_id,to_id):
    try:
        cursor.execute(f"""insert into chats 
                            values 
                            (default,{from_id},{to_id})""")
        connection.commit()

        cursor.execute(f"select chat_id from chats where id1 = {from_id} and id2 = {to_id}")
        fetch = cursor.fetchall()[0][0]
        a = str(fetch)
        cursor.execute(f"""create table chat{a}(
                            msg_id serial primary key,
                            from_id int not null,
                            msg varchar (600) not null,
                            is_read boolean DEFAULT False
                        ) """)
        connection.commit()
        return 'Chat successfully created'
    except:
        return None


def deleteChat(from_id, to_id):
    try:
        cursor.execute(f"delete from chats where (id1 = '{from_id}' and id2 = '{to_id}') or (id1 = '{to_id}' and id2 = '{from_id}')")
        connection.commit()
        chat_id = get_chat_id(from_id, to_id)
        cursor.execute(f"drop table chat{chat_id}")
        connection.commit()
        return 'Chat successfully deleted!'
    except:
        return None


def send_message(chat_id, from_id, text):
    try:
        cursor.execute(f"""insert into chat{chat_id} 
                            values 
                            (default,{from_id},'{text}')""")
        connection.commit()
        return f'Message {text} successfully sent!'
    except:
        return None


def get_chat_id(from_id, to_id):
    try:
        cursor.execute(f"SELECT chat_id FROM chats where (id1 = '{from_id}' and id2 = '{to_id}') or (id1 = '{to_id}' and id2 = '{from_id}')")
        fetch = cursor.fetchall()[0][0]
        return str(fetch)
    except:
        return None

def get_chat(chat_id):
    try:
        update(chat_id)
        cursor.execute(f"SELECT * FROM chat{chat_id}")
        fetch = cursor.fetchall()
        return fetch
    except:
        return None

def get_messages(chat_id,user_id):
    try:
        update(chat_id, user_id)
        chat = f'chat{chat_id}'
        cursor.execute(f"SELECT msg, from_id FROM {chat}")
        fetch = cursor.fetchall()
        return fetch
    except:
        return None



def get_user_contacts(user_id):
    try:
        cursor.execute(f"SELECT contacts FROM info where user_id ={user_id}")
        fetch = cursor.fetchall()[0][0]
        return fetch
    except:
        return None


def get_last_update(chat_id, user_id):
    try:
        cursor.execute(f"SELECT msg, from_id FROM chat{chat_id} where is_read = False")
        fetch = cursor.fetchall()
        update(chat_id, user_id)
        return fetch
    except:
        return None

def update(chat_id,user_id):
    cursor.execute(f"""
                        UPDATE chat{chat_id}
                        SET is_read = True
                        WHERE (is_read = False) and (from_id != {user_id});
                        """)
    connection.commit()


def get_name(user_id):
    try:
        cursor.execute(f"SELECT name FROM info where user_id = {user_id}")
        fetch = cursor.fetchall()[0][0]
        return fetch
    except:
        return None



    
