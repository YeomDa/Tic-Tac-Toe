import tkinter
from tkinter import *
import threading

from firebase_admin import firestore

class Session :
    def __init__(self, user, title, isHost):
        self.sessionWindow = Tk()

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

        self.label_host = Label(self.sessionWindow, text='방장')
        self.label_host.grid(row=0, column=0)

        self.label_host_name = Label(self.sessionWindow, text=self.host_name)
        self.label_host_name.grid(row=1, column=0)

        self.label_guest = Label(self.sessionWindow, text='도전자')
        self.label_guest.grid(row=0, column=1)
        
        if(isHost) :
            self.label_guest_name = Label(self.sessionWindow, text='기다리는 중..')
            
            self.callback_done = threading.Event()
        
            def on_snapshot(doc_snapshot, changes, read_time):
                for doc in doc_snapshot:
                    list = doc.to_dict()
                    self.is_guest_join = True
                    self.guest_name = list.get('GUEST')
                    self.guest_uid = list.get('GUEST_UID')
                    if(self.guest_name != None) :
                        self.label_guest_name.configure(text=self.guest_name)
                self.callback_done.set()

            doc_ref = self.db.collection(u'game_server').document(u'sessions').collection(title).document(u'users')
            doc_watch = doc_ref.on_snapshot(on_snapshot)
       
        else :
            self.label_guest_name = Label(self.sessionWindow, text=self.user.display_name)
        self.label_guest_name.grid(row=1, column=1)

        if(isHost) :
            self.button_game_start = Button(self.sessionWindow, text='게임시작', command=self.game_start)
            self.button_game_start.grid(row=2, column=0, columnspan=2)
        else :
            self.label_wait = Label(self.sessionWindow, text='호스트가 게임을 시작하기를 기다리는 중입니다.')
            self.label_wait.grid(row=2, column=0, columnspan=2)

    def mainloop(self):
        self.sessionWindow.mainloop()

    def game_start(self):
        if(self.is_guest_join) :
            print('게임 시작 가능')
        else :
            print('아직 도전자가 접속하지 않았습니다.')