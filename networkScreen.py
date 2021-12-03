import threading
import socket
from tkinter import *
from winsound import PlaySound
import firebase_admin
from firebase_admin import credentials, auth, db
import main
import socket
import datetime

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
        self.myip = socket.gethostbyname(socket.gethostname())

        #self.default_app = default_app
        print('\n네트워크 설정 화면 진입.')

        print('유저 이메일 :', user.email)
        print('유저 UID :', user.uid)
        print('유저 닉네임 :', user.display_name)
        ref = db.reference(user.uid).child('play_game_count')
        self.play_game_count = ref.get()

    def connect(self, ip):
        print(str(ip) + ' : ' + str(Network.PORT) + '에 연결을 시도합니다.')
        self.append_log(str(ip) + ' : ' + str(Network.PORT) + '에 연결을 시도합니다.')
        self.conn_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_soc.connect((ip, Network.PORT))
        self.append_log(self.conn_soc.getsockname())

    def setWindow(self):
        self.networkWindow = Tk()
        self.networkWindow.title('게임 선택 창')
        self.networkWindow.geometry('750x500')

        self.label_info = Label(self.networkWindow, text='네트워크 설정 화면')
        self.label_info.grid(row=0, columnspan=3)

        self.label_myip = Label(self.networkWindow, text='나의 ip :' + self.myip)
        self.label_myip.grid(row=1, columnspan=3)

        self.label_ip = Label(self.networkWindow, text='상대방의 ip를 입력해주세요.', textvariable='center')
        self.label_ip.grid(row=2, columnspan=3)

        self.entry_ip = Entry(self.networkWindow, width=25)
        self.entry_ip.grid(row=3, column=0, columnspan=2)

        self.button_connect = Button(self.networkWindow, text='연결', command= lambda: self.connect(self.entry_ip.get()))
        self.button_connect.grid(row=3, column=2)

        self.label_my_total = Label(self.networkWindow, text='나의 전적')
        self.label_my_total.grid(row=4, column=0)

        self.label_enemy_total = Label(self.networkWindow, text='상대의 전적')
        self.label_enemy_total.grid(row=4, column=1)

        self.label_my_total_play = Label(self.networkWindow, text='플레이 수 :' + str(self.play_game_count))
        self.label_my_total_play.grid(row=5, column=0)

        self.label_enemy_total_play = Label(self.networkWindow, text='플레이 수 : 임시')
        self.label_enemy_total_play.grid(row=5, column=1)

        self.button_game_start = Button(self.networkWindow, text='게임 시작', bg='blue', fg='white',command=self.game_start)
        self.button_game_start.grid(row=6,columnspan=3)

        self.scroll = Scrollbar(self.networkWindow, orient='vertical')
        self.lbox = Listbox(self.networkWindow, yscrollcommand=self.scroll.set, width=70)
        self.scroll.config(command=self.lbox.yview)
        self.lbox.grid(row=0, column=4, rowspan=7)

        self.append_log(self.user.display_name + '님 환영합니다.')

        #self.myChat.bind('<Return>', self.sendMsg)

    #로그창에 로그를 삽입합니다.
    def append_log(self, msg):
        global now
        self.now = str(datetime.datetime.now())[0:-7]
        self.lbox.insert(END, "[{}] {}".format(self.now, msg))
        self.lbox.update()
        self.lbox.see(END)

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

        