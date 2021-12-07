from tkinter import *
import tkinter
import firebase_admin
import networkScreen

class Lobby() :
    def __init__(self, user) :
        #유저의 정보가 저장된 객체입니다
        self.user = user

        self.lobbyWindow = Tk()
        self.lobbyWindow.title('로비화면')
        self.lobbyWindow.geometry('250x150')

        #유저 닉네임과 함께 환영 메시지를 출력합니다
        self.label_welcome = Label(self.lobbyWindow, text=self.user.display_name + "님 환영합니다.", font=('돋음', 10))
        self.label_welcome.grid(columnspan= 2, row = 0)

        #네트워크 3목
        self.button_network_3 = Button(self.lobbyWindow, text='네트워크 3목', bg='blue', fg='white', command= lambda: self.select_mode('network_3'))
        self.button_network_3.grid(columnspan = 2 , row = 1)

        #네트워크 5목
        self.button_network_5 = Button(self.lobbyWindow, text='네트워크 5목', bg='blue', fg='white', command= lambda: self.select_mode('network_5'))
        self.button_network_5.grid(columnspan = 2, row = 2)

        #로컬 3목
        self.button_local_3 = Button(self.lobbyWindow, text='로컬 3목', bg='blue', fg='white', command= lambda: self.select_mode('local_3'))
        self.button_local_3.grid(columnspan = 2 , row = 3)
        
        #로컬 5목
        self.button_local_5 = Button(self.lobbyWindow, text='로컬 5목', bg='blue', fg='white', command= lambda: self.select_mode('local_5'))
        self.button_local_5.grid(columnspan = 2, row = 4)

    def mainloop(self) :
        self.lobbyWindow.mainloop()

    def select_mode(self, mode) :
        if mode == 'network_3' :
            print('network_3 모드를 선택하였습니다.')
            self.lobbyWindow.destroy() #로비 화면 종료
            network_screen = networkScreen.Network(self.user, mode)
            network_screen.run()

        elif mode == 'network_5' :
            print('network_5 모드를 선택하였습니다.')
            self.lobbyWindow.destroy()
            network_screen = networkScreen.Network(self.user,mode)
            network_screen.run()

        elif mode == 'local_3' :
            print('local_3 모드를 선택하였습니다.')
            self.lobbyWindow.destroy()
            main.l_main(3)
        elif mode == 'local_5' :
            print('local_5 모드를 선택하였습니다.')
            self.lobbyWindow.destroy()
            main.l_main(4)
        else :
            print('게임모드 선택 매개변수가 잘못 전달되었습니다.'
        