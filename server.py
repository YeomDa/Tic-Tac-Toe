import pickle
import socket, threading
import firebase_admin
from firebase_admin import credentials, auth, db
from tkinter import *
import os
import sys

cred = credentials.Certificate("firebase/opensw-team1-firebase-adminsdk-ln99u-734bf11a84.json")
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://opensw-team1-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

class Room:
    def __init__(self):
        self.gamers = []
        self.allChat=None

    def addClient(self, c):  
        self.gamers.append(c)

    def delClient(self, c):
        self.gamers.remove(c)

    def sendMsgAll(self, msg):  
        for i in self.gamers:
            print(i)
            i.sendMsg(msg)

    def disconnectAll(self):
        for i in self.gamers:
            i.disconnect()

#게임 서버 접속자
class Client:  
    def __init__(self, r, soc):
        self.room = r 
        self.id = None
        self.soc = soc  
        self.user = None

    #서버가 접속자에게서 메시지를 읽습니다
    def readMsg(self):
        while True:
            try :
                msg = self.soc.recv(1024).decode(encoding='utf-8')

                if(msg == '/stop_server') :
                    db.reference('server_info').child('is_server_open').set('False')
                    raise Exception('프로그램 종료')
                
                print('메시지를 읽었습니다. :', msg)
                self.sendMsg(msg)

            except ConnectionResetError as e :
                self.room.delClient(self)
                self.soc.close()
                break
            '''
            msg = self.id + '님이 입장하셨습니다'
            self.room.sendMsgAll(msg)

            while True:
                msg = self.soc.recv(1024).decode()  
                if msg == '/stop': 
                    self.soc.sendall(msg)  
                    self.room.delClient(self)
                    break
                msg = self.id+': '+ msg
                self.room.sendMsgAll(msg)  
            self.room.sendMsgAll(self.id + '님이 퇴장하셨습니다.')
            '''
    
    #서버가 접속자에게 메시지를 보냅니다
    def sendMsg(self, msg):
        print('메시지를 보냅니다. :', msg)
        self.soc.sendall(msg.encode(encoding='utf-8'))

    def disconnect(self):
        self.soc.close()

#서버에게 보여지는 화면
class GameServer:
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 9999
    is_another_server_online = False

    def __init__(self):
        if(db.reference('server_info').child('is_server_open').get() == 'True') :
            print('서버가 이미 열려있습니다.')
            return

        db.reference('server_info').child('current_server_ip').set(self.HOST)
        db.reference('server_info').child('is_server_open').set('True')

        self.server_soc = None  
        self.room = Room()

        self.run()

    def open(self):
        self.server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_soc.bind((GameServer.HOST, GameServer.PORT))
        self.server_soc.listen()

    def run(self):
        self.open()
        print('서버 시작')

        while True:
            client_soc, addr = self.server_soc.accept()
            print(addr, '접속')
            c = Client(self.room, client_soc)
            self.room.addClient(c)
            print('접속자 수:', len(self.room.gamers))
            c.sendMsg('[Server] : 접속을 환영합니다.')
            th = threading.Thread(target=c.readMsg)
            th.start()

        #self.server_soc.close()

def main():
    GameServer()

main()