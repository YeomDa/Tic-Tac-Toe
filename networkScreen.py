from tkinter import *
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

        self.db = firestore.client()
        
        doc_ref = self.db.collection(u'user_info').document(user.uid)
        doc = doc_ref.get()
        if doc.exists:
            self.play_game_count = doc.to_dict()['play_game_count']
            print(self.play_game_count)
            print(f'Document data: {doc.to_dict()}')
        else:
            print(u'No such document!')
            
    def setWindow(self):
        self.networkWindow = Tk()
        self.networkWindow.title('게임 선택 창')
        self.networkWindow.geometry('750x500')

        self.label_info = Label(self.networkWindow, text='네트워크 설정 화면')
        self.label_info.grid(row=0, column=0)

        self.label_my_total = Label(self.networkWindow, text='나의 전적')
        self.label_my_total.grid(row=1, column=0)

        self.label_my_total_play = Label(self.networkWindow, text='플레이 수 :' + str(self.play_game_count))
        self.label_my_total_play.grid(row=2, column=0)

        self.button_send = Button(self.networkWindow, text='방 생성', width=20, 
        command=lambda: self.create_room(self.user.display_name, self.user.uid))
        self.button_send.grid(row=3, column=0)

        self.entry_room_name = Entry(self.networkWindow, width=10)
        self.entry_room_name.grid(row=4, column=0)

        self.button_game_start = Button(self.networkWindow, text='방 입장', bg='blue', fg='white',
        command=lambda: self.enter_room(self.entry_room_name.get()))
        self.button_game_start.grid(row=5,column=0)

    def run(self):
        self.setWindow()
        self.networkWindow.mainloop()
    
    def create_room(self, title, uid):
        print('방생성 :', title)
        data = {
            u'HOST' : title,
            u'HOST_UID' : uid 
        }
        self.db.collection(u'game_server').document('sessions').collection(title).document('users').set(data)

        print('network_3 모드를 선택하였습니다.')
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