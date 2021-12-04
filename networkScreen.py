from tkinter import *
import tkinter.font as tkFont
from firebase_admin import firestore
import sessionScreen

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

        print('유저 이메일 :', user.email)
        print('유저 UID :', user.uid)
        print('유저 닉네임 :', user.display_name)

        #데이터베이스 클라이언트 생성
        self.db = firestore.client()
        #firebase 데이터베이스의 경로를 지정합니다 (user_info/사용자uid)
        doc_ref = self.db.collection(u'user_info').document(user.uid)
        #해당 데이터베이스 경로의 데이터를 가져옵니다
        doc = doc_ref.get()
        #해당 경로가 존재한다면,
        if doc.exists:
            data_list = doc.to_dict()
            self.play_game_count = data_list.get('play_game_count') #경로의 데이터를 list화 시키고, 'play_game_count'의 값을 가져옵니다.
            self.win_count = data_list.get('win_count')
            self.tie_count = data_list.get('tie_count')
            self.defeat_count = data_list.get('defeat_count')
            print(f'전적 : {data_list}') #해당 경로의 모든 데이터를 출력합니다
        else:
            print(u'No such document!')
        
        if(self.play_game_count == None) : self.play_game_count = 0
        if(self.win_count == None) : self.win_count = 0
        if(self.tie_count == None) : self.tie_count = 0
        if(self.defeat_count == None) : self.defeat_count = 0

    def setWindow(self):
        self.networkWindow = Tk()
        self.networkWindow.title('게임 선택 창')
        self.networkWindow.geometry('250x300')

        self.label_info = Label(self.networkWindow, text='네트워크 대전 로비 화면', height=2)
        info_font = tkFont.Font(family="Arial", size=16, weight="bold")
        self.label_info.configure(font=info_font)
        self.label_info.grid(row=0, column=0, columnspan=2)

        self.label_my_total = Label(self.networkWindow, text='닉네임 : ' + self.user.display_name)
        self.label_my_total.grid(row=1, column=0, columnspan=2)

        self.label_my_total_play = Label(self.networkWindow, text='총 게임 수 :' + str(self.play_game_count))
        self.label_my_total_play.grid(row=2, column=0, columnspan=2)

        self.label_my_win = Label(self.networkWindow, text='승리 :' + str(self.win_count))
        self.label_my_win.grid(row=3, column=0, columnspan=2)

        self.label_my_tie = Label(self.networkWindow, text='무승부 :' + str(self.tie_count))
        self.label_my_tie.grid(row=4, column=0, columnspan=2)

        self.label_my_defeat = Label(self.networkWindow, text='패배 :' + str(self.defeat_count))
        self.label_my_defeat.grid(row=5, column=0, columnspan=2)

        if(self.win_count == 0):
            self.win_rate = '0.0%'
        else:
            self.win_rate = str(self.play_game_count / self.win_count * 100) + '%'
        self.label_my_win_rate = Label(self.networkWindow, text='승률 :' + self.win_rate)
        self.label_my_win_rate.grid(row=6, column=0, columnspan=2)

        self.button_send = Button(self.networkWindow, text='방 생성', width=15, bg='blue', fg='white',
        command=lambda: self.create_room(self.user.display_name, self.user.uid))
        self.button_send.grid(row=7, column=0, columnspan=2, pady=10)

        self.entry_room_name = Entry(self.networkWindow, width=20)
        self.entry_room_name.grid(row=8, column=0, pady=10)

        self.button_game_start = Button(self.networkWindow, text='방 입장', bg='blue', fg='white',
        command=lambda: self.enter_room(self.entry_room_name.get()))
        self.button_game_start.grid(row=8,column=1, pady=10)

    def run(self):
        self.setWindow()
        self.networkWindow.mainloop()
    
    def create_room(self, title, uid):
        db_ref = self.db.collection(u'game_server').document('sessions').collection(title)
        if(db_ref.document('game_start').get().exists):
            self.db.collection(u'game_server').document('sessions').collection(title).document('game_start').update({
                u'is_game_start' : firestore.DELETE_FIELD
            })

        if(db_ref.document('game_log').get().exists):
            self.db.collection(u'game_server').document('sessions').collection(title).document('game_log').update({
                u'landing_position_x' : firestore.DELETE_FIELD,
                u'landing_position_y' : firestore.DELETE_FIELD,
                u'turn' : firestore.DELETE_FIELD
            })

        print('방 생성 :', title)
        #firebase의 데이터는 key-value형태로 저장됩니다.
        data = {
            u'HOST' : title,
            u'HOST_UID' : uid 
        }

        #해당 경로에 데이터를 .set 합니다.
        self.db.collection(u'game_server').document('sessions').collection(title).document('users').set(data)
        self.db.collection(u'game_server').document('sessions').collection(title).document('game_start').set({
            u'is_game_start' : False
        }, merge=True)

        self.networkWindow.destroy() #로비 화면 종료
        session_screen = sessionScreen.Session(self.user, title, True)
        session_screen.mainloop()

    def enter_room(self, title):
        db_ref = self.db.collection(u'game_server').document(u'sessions').collection(title)
        doc = db_ref.get()
        if(bool(doc)):
            self.networkWindow.destroy() #로비 화면 종료
            session_screen = sessionScreen.Session(self.user, title, False)
            session_screen.mainloop()

        print('입장 :',title)

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