import tkinter
from tkinter import *
import threading
from firebase_admin import firestore
import main

class Session :
    def __init__(self, user, title, isHost):
        self.sessionWindow = Tk()
        self.sessionWindow.geometry('270x200')

        self.isHost = isHost
        self.title = title
        self.user = user
        self.db = firestore.client()

        if(isHost) :
            self.host_name = user.display_name
            self.is_guest_join = False
            self.guest_name = None
            self.guest_uid = None
        else :
            db_ref = self.db.collection(u'game_server').document(u'sessions').collection(title).document(u'users')
            self.host_name = db_ref.get().to_dict()['HOST']
            self.host_uid = db_ref.get().to_dict()['HOST_UID']
            db_ref.set({
                u'GUEST' : self.user.display_name,
                u'GUEST_UID' : self.user.uid
            }, merge=True)
        
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
        
        if(isHost) :
            my_column = 0
        else :
            my_column = 1

        self.label_host = Label(self.sessionWindow, text='방장')
        self.label_host.grid(row=0, column=0)

        self.label_host_name = Label(self.sessionWindow, text=self.host_name)
        self.label_host_name.grid(row=1, column=0)

        self.label_my_total_play = Label(self.sessionWindow, text='총 게임 수 :' + str(self.play_game_count))
        self.label_my_total_play.grid(row=2, column=my_column)

        self.label_my_win = Label(self.sessionWindow, text='승리 :' + str(self.win_count))
        self.label_my_win.grid(row=3, column=my_column)

        self.label_my_tie = Label(self.sessionWindow, text='무승부 :' + str(self.tie_count))
        self.label_my_tie.grid(row=4, column=my_column)

        self.label_my_defeat = Label(self.sessionWindow, text='패배 :' + str(self.defeat_count))
        self.label_my_defeat.grid(row=5, column=my_column)

        if(self.win_count == 0):
            self.win_rate = '0.0%'
        else:
            self.win_rate = str(self.play_game_count / self.win_count * 100) + '%'
        self.label_my_win_rate = Label(self.sessionWindow, text='승률 :' + self.win_rate)
        self.label_my_win_rate.grid(row=6, column=my_column)

        self.label_guest = Label(self.sessionWindow, text='도전자')
        self.label_guest.grid(row=0, column=1)
        
        if(isHost) :
            self.label_guest_name = Label(self.sessionWindow, text='기다리는 중..')
            
            callback_done = threading.Event()
            #데이터가 변경되면 호출되는 콜벡 메서드
            def on_snapshot(doc_snapshot, changes, read_time):
                for doc in doc_snapshot:
                    list = doc.to_dict()
                    self.is_guest_join = True
                    self.guest_name = list.get('GUEST')
                    self.guest_uid = list.get('GUEST_UID')
                    if(self.guest_name != None) :
                        self.label_guest_name.configure(text=self.guest_name)

                        doc_guest_ref = self.db.collection(u'user_info').document(self.guest_uid)
                        doc_guest = doc_guest_ref.get()
                        if doc_guest.exists:
                            guest_data_list = doc_guest.to_dict()
                            guest_play_game_count = guest_data_list.get('play_game_count') #경로의 데이터를 list화 시키고, 'play_game_count'의 값을 가져옵니다.
                            guest_win_count = guest_data_list.get('win_count')
                            guest_tie_count = guest_data_list.get('tie_count')
                            guest_defeat_count = guest_data_list.get('defeat_count')
                            print(f'상대 전적 : {guest_data_list}') #해당 경로의 모든 데이터를 출력합니다
                        else:
                            print(u'No such document!')
                        if(guest_play_game_count == None) : guest_play_game_count = 0
                        if(guest_win_count == None) : guest_win_count = 0
                        if(guest_tie_count == None) : guest_tie_count = 0
                        if(guest_defeat_count == None) : guest_defeat_count = 0
                        
                        label_guest_total_play = Label(self.sessionWindow, text='총 게임 수 :' + str(guest_play_game_count))
                        label_guest_total_play.grid(row=2, column=1)

                        guest_label_guest_win = Label(self.sessionWindow, text='승리 :' + str(guest_win_count))
                        guest_label_guest_win.grid(row=3, column=1)

                        guest_label_guest_tie = Label(self.sessionWindow, text='무승부 :' + str(guest_tie_count))
                        guest_label_guest_tie.grid(row=4, column=1)

                        guest_label_guest_defeat = Label(self.sessionWindow, text='패배 :' + str(guest_defeat_count))
                        guest_label_guest_defeat.grid(row=5, column=1)

                        if(guest_win_count == 0):
                            guest_win_rate = '0.0%'
                        else:
                            guest_win_rate = str(guest_play_game_count / guest_win_count * 100) + '%'
                        guest_label_guest_win_rate = Label(self.sessionWindow, text='승률 :' + guest_win_rate)
                        guest_label_guest_win_rate.grid(row=6, column=1)

                callback_done.set()

            doc_ref = self.db.collection(u'game_server').document(u'sessions').collection(title).document(u'users') #변경을 감지할 데이터베이스 주소입니다.
            doc_watch = doc_ref.on_snapshot(on_snapshot) #이친구가 doc_ref경로의 데이터가 변경되면 on_snapshot 메서드를 실행합니다.
       
        else :
            self.label_guest_name = Label(self.sessionWindow, text=self.user.display_name)
            callback_done = threading.Event()
            #데이터가 변경되면 호출되는 콜벡 메서드
            def on_snapshot(doc_snapshot, changes, read_time):
                for doc in doc_snapshot:
                    list = doc.to_dict()
                    host_name = list.get('HOST')
                    host_uid = list.get('HOST_UID')
                    if(host_name != None) :
                        doc_host_ref = self.db.collection(u'user_info').document(host_uid)
                        doc_host = doc_host_ref.get()
                        if doc_host.exists:
                            host_data_list = doc_host.to_dict()
                            host_play_game_count = host_data_list.get('play_game_count') #경로의 데이터를 list화 시키고, 'play_game_count'의 값을 가져옵니다.
                            host_win_count = host_data_list.get('win_count')
                            host_tie_count = host_data_list.get('tie_count')
                            host_defeat_count = host_data_list.get('defeat_count')
                            print(f'상대 전적 : {host_data_list}') #해당 경로의 모든 데이터를 출력합니다
                        else:
                            print(u'No such document!')
                        if(host_play_game_count == None) : host_play_game_count = 0
                        if(host_win_count == None) : host_win_count = 0
                        if(host_tie_count == None) : host_tie_count = 0
                        if(host_defeat_count == None) : host_defeat_count = 0
                        
                        label_host_total_play = Label(self.sessionWindow, text='총 게임 수 :' + str(host_play_game_count))
                        label_host_total_play.grid(row=2, column=0)

                        guest_label_host_win = Label(self.sessionWindow, text='승리 :' + str(host_win_count))
                        guest_label_host_win.grid(row=3, column=0)

                        guest_label_host_tie = Label(self.sessionWindow, text='무승부 :' + str(host_tie_count))
                        guest_label_host_tie.grid(row=4, column=0)

                        guest_label_host_defeat = Label(self.sessionWindow, text='패배 :' + str(host_defeat_count))
                        guest_label_host_defeat.grid(row=5, column=0)

                        if(host_win_count == 0):
                            host_win_rate = '0.0%'
                        else:
                            host_win_rate = str(host_play_game_count / host_win_count * 100) + '%'
                        guest_label_host_defeat = Label(self.sessionWindow, text='승률 :' + host_win_rate)
                        guest_label_host_defeat.grid(row=6, column=0)

                callback_done.set()

            doc_ref = self.db.collection(u'game_server').document(u'sessions').collection(title).document(u'users') #변경을 감지할 데이터베이스 주소입니다.
            doc_watch = doc_ref.on_snapshot(on_snapshot) #이친구가 doc_ref경로의 데이터가 변경되면 on_snapshot 메서드를 실행합니다.
        self.label_guest_name.grid(row=1, column=1)

        self.button_game_start = Button(self.sessionWindow, text='게임시작', command=lambda: self.game_start(self.title)) #호스트가 아니면 화면엔 안띄움
        if(isHost) :
            self.button_game_start.grid(row=7, column=0, columnspan=2)
        else :
            self.label_wait = Label(self.sessionWindow, text='호스트가 게임을 시작하기를 기다리는 중입니다.')
            self.label_wait.grid(row=7, column=0, columnspan=2)

            self.callback_done = threading.Event()
            def on_snapshot(doc_snapshot, changes, read_time):
                for doc in doc_snapshot:
                    list = doc.to_dict()
                    is_game_start = list.get('is_game_start')
                    print(is_game_start)
                    if(is_game_start):
                        self.not_host_start()

                self.callback_done.set()

            doc_ref = self.db.collection(u'game_server').document(u'sessions').collection(title).document(u'game_start')
            self.doc_watch = doc_ref.on_snapshot(on_snapshot) #이친구가 doc_ref경로의 데이터가 변경되면 on_snapshot 메서드를 실행합니다.
            
    def not_host_start(self):
        self.button_game_start.invoke()

    def mainloop(self):
        self.sessionWindow.mainloop()

    def game_start(self, title):
        if(self.isHost == False) :
            print('도전자 게임 입장')
            self.doc_watch.unsubscribe()
            self.callback_done.set()
            self.sessionWindow.destroy() #세션 화면 종료
            main.main(title, self.user)

        if(self.is_guest_join) :
            print('게임 시작 가능')
            
            self.db.collection(u'game_server').document('sessions').collection(title).document('game_start').set({
                u'is_game_start' : True
            }, merge=True)

            self.sessionWindow.destroy() #세션 화면 종료
            main.main(title, self.user)
        else :
            print('아직 도전자가 접속하지 않았습니다.')