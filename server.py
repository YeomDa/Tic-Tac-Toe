import socket, threading

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

#접속자에게 보여지는 화면
class ChatClient:  
    def __init__(self, r, soc):
        self.room = r 
        self.id = None
        self.soc = soc  

    def readMsg(self):
        self.id = self.soc.recv(1024).decode()
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

    def sendMsg(self, msg):
        print(type(msg))
        self.soc.sendall(msg.encode(encoding='utf-8'))

#서버에게 보여지는 화면
class ChatServer:
    HOST = '127.0.0.1'  
    PORT = 9999

    def __init__(self):
        self.server_soc = None  
        self.room = Room()

    def open(self):
        self.server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_soc.bind((ChatServer.HOST, ChatServer.PORT))
        self.server_soc.listen()

    def run(self):
        self.open()
        print('서버 시작')

        while True:
            client_soc, addr = self.server_soc.accept()
            print(addr, '접속')
            c = ChatClient(self.room, client_soc)
            self.room.addClient(c)
            print('접속자:',self.room.gamers)
            th = threading.Thread(target=c.readMsg)
            th.start()

        #self.server_soc.close()


def main():
    cs = ChatServer()
    cs.run()

main()