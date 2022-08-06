import requests
import json

class User:
    def __init__(self, user_id):
        self.id, self.name = requests.get(f'http://127.0.0.1:5000/info?id={user_id}').json().values()
        self.contacts = requests.get(f'http://127.0.0.1:5000/contacts?id={user_id}').content.decode('utf-8').split(',')

