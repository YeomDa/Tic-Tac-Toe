import threading
import socket
from tkinter import *
from winsound import PlaySound
import firebase_admin
from firebase_admin import credentials, auth, db
import main

class Choice():
    HOST = '127.0.0.1'
    PORT = 9999

    def __init__(self, user, default_app):
        self.user = user
        self.conn_soc = None
        self.chatCont = None
        self.myChat = None
        self.sendBtn = None
        self.allChat =''

        self.default_app = default_app
        print('\n게임서버가 열렸습니다.')

        print('유저 이메일 :', user.email)
        print('유저 UID :', user.uid)
        print('유저 닉네임 :', user.display_name)
        ref = db.reference(user.uid).child('play_game_count')
        self.play_game_count = ref.get()

    def conn(self):
        self.conn_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_soc.connect((Choice.HOST, Choice.PORT))

    def setWindow(self):
        self.choiceWindow = Tk()
        self.choiceWindow.title('게임 선택 창')
        self.choiceWindow.geometry('600x500+300+300')

        self.button_game1 = Button(self.choiceWindow, text='TIC_TAC_TOE', bg='blue', fg='white',command=self.game1in)
        self.button_game1.grid(row=1,column=0)
        self.button_game2 = Button(self.choiceWindow, text='GAME2', bg='blue', fg='white')
        self.button_game2.grid(row=1,column=1)
        self.button_game3 = Button(self.choiceWindow, text='GAME3', bg='blue', fg='white')
        self.button_game3.grid(row=1,column=2)

        self.chatCont = Label(self.choiceWindow, width=50, height=10, text='접속확인을 위해 임시로 만듦')
        self.chatCont.grid(row=3,column=0,columnspan=2)
        self.myChat = Entry(self.choiceWindow, width=40)
        self.myChat.grid(row=4,column=0, padx=10)
        self.myChat.insert(END,self.user.display_name)
        self.sendBtn = Button(self.choiceWindow, width=10, text='전송')
        self.sendBtn.grid(row=4, column=1)

        self.myChat.bind('<Return>', self.sendMsg)

    def sendMsg(self, e):  

        msg = self.myChat.get()
        self.myChat.delete(0, END)
        self.myChat.config(text='')
        print(type(msg))
        msg = msg.encode(encoding='utf-8')
        print(self.conn_soc)
        self.conn_soc.sendall(msg)
        print('전송')
        
    def recvMsg(self):  
        while True:
            print('keep going')
            msg = self.conn_soc.recv(1024)
            print(msg)
            msg = msg.decode()+'\n'
            self.allChat += msg
            print(',:', self.allChat)

            self.chatCont.config(text=self.allChat)

    def run(self):
        self.conn()
        self.setWindow()

        th2 = threading.Thread(target=self.recvMsg)
        th2.start()
        self.choiceWindow.mainloop()

    def game1in(self):
        self.choiceWindow.destroy()  
        main.Tic_Tac_Toe.mainloop()