import threading
import socket
from tkinter import *
from winsound import PlaySound
import firebase_admin
from firebase_admin import credentials, auth, db
import main

class Network():
    #HOST = ''
    PORT = 9999

    def __init__(self, user, mode):
        self.user = user
        self.mode = mode
        self.conn_soc = None
        self.chatCont = None
        self.myChat = None
        self.sendBtn = None
        self.allChat =''

        #self.default_app = default_app
        print('\n네트워크 설정 화면 진입.')

        print('유저 이메일 :', user.email)
        print('유저 UID :', user.uid)
        print('유저 닉네임 :', user.display_name)
        ref = db.reference(user.uid).child('play_game_count')
        self.play_game_count = ref.get()

    def conn(self, ip):
        print(str(ip) + ' : ' + str(Network.PORT) + '에 연결을 시도합니다.')
        self.conn_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_soc.connect((ip, Network.PORT))

    def setWindow(self):
        self.networkWindow = Tk()
        self.networkWindow.title('게임 선택 창')
        self.networkWindow.geometry('600x500+300+300')

        self.label_info = Label(self.networkWindow, text='네트워크 설정 화면')
        self.label_info.grid(row=0, columnspan=3)

        self.label_ip = Label(self.networkWindow, text='상대방의 ip를 입력해주세요.', textvariable='center')
        self.label_ip.grid(row=1, columnspan=3)

        self.entry_ip = Entry(self.networkWindow, width=25)
        self.entry_ip.grid(row=2, column=0, columnspan=2)

        self.button_connect = Button(self.networkWindow, text='연결', command= lambda: self.conn(self.entry_ip.get()))
        self.button_connect.grid(row=2, column=2)

        self.label_my_total = Label(self.networkWindow, text='나의 전적')
        self.label_my_total.grid(row=3, column=0)

        self.label_enemy_total = Label(self.networkWindow, text='상대의 전적')
        self.label_enemy_total.grid(row=3, column=1)

        self.label_my_total_play = Label(self.networkWindow, text='플레이 수 :' + str(self.play_game_count))
        self.label_my_total_play.grid(row=4, column=0)

        self.label_enemy_total_play = Label(self.networkWindow, text='플레이 수 : 임시')
        self.label_enemy_total_play.grid(row=4, column=1)

        self.button_game_start = Button(self.networkWindow, text='게임 시작', bg='blue', fg='white',command=self.game_start)
        self.button_game_start.grid(row=5,columnspan=3)

        #self.myChat.bind('<Return>', self.sendMsg)

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
        #self.conn()
        self.setWindow()

        #th2 = threading.Thread(target=self.recvMsg)
        #th2.start()
        #self.choiceWindow.mainloop()

    def game_start(self):
        if(self.mode == 'network_3') :
            print('네트워크 3목 게임을 실행합니다.')
            #self.networkWindow.destroy()  
            #main.Tic_Tac_Toe.mainloop()
        elif(self.mode == 'network_5') :
            print('네트워크 5목 게임을 실행합니다.')
            #self.networkWindow.destroy()  
            #main.Tic_Tac_Toe.mainloop()
        else :
            print('네트워크 설정 화면에서 게임 실행 시 잘못된 모드 매개변수가 전달되었습니다.')

        