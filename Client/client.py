from ast import Str
from time import sleep
from tkinter import *
from pandas import array
import requests
import core
import ast
import threading
import time


class Registaration_window:
	def __init__(self, main_window):
		self.window=Toplevel(main_window)
		self.window.title('Register')
		self.window.geometry('400x300')
		

		self.login = Text(self.window,
						height = 1,
						width = 20)
		self.login.pack()

		self.password = Text(self.window,
							height = 1,
							width = 20)
		self.password.pack()

		self.repeat_password = Text(self.window,
							height = 1,
							width = 20)
		self.repeat_password.pack()

		self.register_button = Button(self.window,
								text = "Register", 
								command = self.register)

		self.register_button.pack()

		self.lbl = Label(self.window, text = "")
		self.lbl.pack()

	def register(self):
		if self.password.get(1.0, "end-1c") == self.repeat_password.get(1.0, "end-1c"):
			requests.post('http://127.0.0.1:5000/register', json={'login': self.login.get(1.0, "end-1c"), 'password': self.password.get(1.0, "end-1c")})
			self.window.destroy()
		else:
			self.lbl.config(text = "Passwords did not match")


class ChatWindow:
	def __init__(self,main_window, from_user, to_user):
		self.from_user = from_user
		self.to_user = to_user
		self.chat_window=Toplevel(main_window)
		self.chat_window.rowconfigure(1, weight=1)
		self.chat_window.title('Chat with ' + self.to_user.name)
		self.chat_window.geometry('400x300')
		self.chat_id = self.get_chat_id()
		self.chat_window.columnconfigure(0, weight=1)
		self.chat_window.rowconfigure(0, weight=1)
		self.scroll = Scrollbar(self.chat_window, orient = 'vertical')
		self.scroll.pack(side = RIGHT, fill = Y)
		thread = threading.Thread(target=self.update_func)
		thread.start()

		self.msg = Text(self.chat_window,
							height = 1,
							width = 20)
		self.msg.place(x=15,y=15)
		self.msg.pack()
		self.send_button = Button(self.chat_window,
								text = "Send", 
								command = lambda: [self.send_message(), self.update_by_click()])
		self.send_button.pack()


		self.msg_list = ast.literal_eval(requests.get(f'http://127.0.0.1:5000/getMessages?chat_id={self.chat_id}&user_id={self.from_user.id}').content.decode('utf-8'))
		for msg in self.msg_list:
			name = requests.get(f'http://127.0.0.1:5000/name?id={msg[1]}').content.decode('utf-8')
			self.lbl = Label(self.chat_window, text = f'{name}: {msg[0]}')
			self.lbl.pack()

	def send_message(self):
		requests.post('http://127.0.0.1:5000/sendMessage', json={'chat_id': self.chat_id, 'from': self.from_user.id, 'text':self.msg.get(1.0, "end-1c")})
	
	def get_chat_id(self):
		return requests.get(f'http://127.0.0.1:5000/getChatId?from={self.from_user.id}&to={self.to_user.id}').content.decode('utf-8')

	def get_last_update(self):

		msgs = ast.literal_eval(requests.get(f'http://127.0.0.1:5000/getLastUpdate?chat_id={self.chat_id}&user_id={self.from_user.id}').content.decode('utf-8'))
		for msg in msgs:
			if str(self.from_user.id) != str(msg[1]):
				name = requests.get(f'http://127.0.0.1:5000/name?id={msg[1]}').content.decode('utf-8')
				self.lbl = Label(self.chat_window, text = f'{name}: {msg[0]}')
				self.lbl.pack()

	def update_by_click(self):
		msgs = ast.literal_eval(requests.get(f'http://127.0.0.1:5000/getLastUpdate?chat_id={self.chat_id}&user_id={self.from_user.id}').content.decode('utf-8'))
		for msg in msgs:
			name = requests.get(f'http://127.0.0.1:5000/name?id={msg[1]}').content.decode('utf-8')
			self.lbl = Label(self.chat_window, text = f'{name}: {msg[0]}')
			self.lbl.pack()

	def update_func(self):
		while True:
			# if self.from_user
			self.get_last_update()
			time.sleep(2)

class Main_window:
	def __init__(self):
		self.window=Tk()
		self.window.title('LisaChat')
		self.window.geometry('400x300')

		self.login = Entry(self.window,
						width = 20)
		self.login.pack()

		self.password = Entry(self.window,
							width = 20)
		self.password.pack()

		self.login_button = Button(self.window,
								text = "Login", 
								command = self.login_func)
		self.login_button.pack()

		self.register_button = Button(self.window,
								text = "Register", 
								command = self.open_registration_window)

		self.register_button.pack()

		self.lbl = Label(self.window, text = "")
		self.lbl.pack()

		self.window.mainloop()

	def open_registration_window(self):
		Registaration_window(self.window)

	def login_func(self):
		login = self.login.get()
		pswd = self.password.get()
		id = requests.get(f'http://127.0.0.1:5000/login?login={login}&password={pswd}').content.decode('utf-8')
		if id:
			self.user = core.User(id)
			self.contacts_window()
		else:
			print('smth bad')


	def contacts_window(self):
		for widget in self.window.winfo_children():
			widget.destroy()

		for id in self.user.contacts:
			name = requests.get(f'http://127.0.0.1:5000/name?id={id}').content

			self.contact_button = Button(self.window,
								text = name, 
								command = lambda id=id: ChatWindow(self.window, core.User(self.user.id), core.User(id)))
			self.contact_button.pack()
	def getlastupdate(self):
		pass
main = Main_window()





