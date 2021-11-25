from tkinter import *
import tkinter
import firebase_admin
from firebase_admin import credentials, auth
import main

cred = credentials.Certificate("firebase/opensw-team1-firebase-adminsdk-ln99u-734bf11a84.json")
default_app = firebase_admin.initialize_app(cred)

class Login() :
    def __init__(self) :
        self.loginWindow = Tk()
        self.loginWindow.title('로그인 및 회원가입')
        #self.loginWindow.geometry('300x100')

        self.label_info = Label(self.loginWindow, text='로그인', font=('돋음', 10))
        self.label_info.grid(columnspan= 2, row = 0)

        self.label_email = Label(self.loginWindow, text='Email', font=('돋음', 10))
        self.label_email.grid(column = 0, row = 1)
        self.entry_email = Entry(self.loginWindow, width = 30)
        self.entry_email.grid(column = 1, row = 1)

        self.label_pwd = Label(self.loginWindow, text='PW', font=('돋음', 10)) 
        self.label_pwd.grid(column = 0, row = 2)
        self.entry_pwd = Entry(self.loginWindow, width = 30)
        self.entry_pwd.grid(column = 1, row = 2)

        self.button_login = Button(self.loginWindow, text='로그인', bg='blue', fg='white', command=self.login)
        self.button_login.grid(columnspan = 2 , row = 4)
        self.button_register = Button(self.loginWindow, text='회원가입', bg='blue', fg='white', command=self.open_register_window)
        self.button_register.grid(columnspan = 2, row = 5)

    def mainloop(self) :
        self.loginWindow.mainloop()

    def login(self) :
        print('로그인 버튼 클릭')
        input_email = self.entry_email.get()
        input_pwd = self.entry_pwd.get()

        if(len(input_email) == 0 or len(input_pwd) == 0) :
            print('이메일 또는 비밀번호를 입력해주세요.')
            return

        user = auth.get_user_by_email(input_email)
        print('로그인이 완료되었습니다.')
        print('이메일 :', user.email)
        print('UID :', user.uid)
        print('닉네임 :', user.display_name)

        self.loginWindow.destroy()
        game_instance = main.Tic_Tac_Toe(user=user)
        game_instance.mainloop()
        
    
    def register(self) :
        input_email = self.entry_reg_email.get()
        input_pwd = self.entry_reg_password.get()
        input_confirm_pwd = self.entry_reg_confirm_password.get()
        input_nickname = self.entry_reg_nickname.get()

        if(len(input_email) == 0 or len(input_pwd) == 0 or len(input_confirm_pwd) == 0 or len(input_nickname) == 0) :
            print('모든 입력창에 정보를 입력해주세요.')
            return
            
        if(input_pwd.__eq__(input_confirm_pwd) == False) :
            print("비밀번호 틀림")
            return
        
        user = auth.create_user(email=input_email, password=input_pwd, display_name=input_nickname)
        print('회원가입이 완료되었습니다.')
        print('이메일 :', user.email)
        print('UID :', user.uid)
        print('닉네임 :', user.display_name)
        self.registerWindow.destroy()

    def open_register_window(self) :
        print('회원가입 버튼 클릭')

        self.registerWindow = tkinter.Toplevel(self.loginWindow)
        #toplevel.geometry('350x350')
        
        self.label_reg_register = Label(self.registerWindow, text='회원가입')
        self.label_reg_register.grid(columnspan=2, row=0)

        self.label_reg_nickname = Label(self.registerWindow, text='Nickname')
        self.label_reg_nickname.grid(column=0, row=1)
        self.entry_reg_nickname = Entry(self.registerWindow, width=30)
        self.entry_reg_nickname.grid(column=1, row=1)

        self.label_reg_email = Label(self.registerWindow, text='Email')
        self.label_reg_email.grid(column=0, row=2)
        self.entry_reg_email = Entry(self.registerWindow, width=30)
        self.entry_reg_email.grid(column=1, row=2)

        self.label_reg_password = Label(self.registerWindow, text='Password')
        self.label_reg_password.grid(column=0, row=3)
        self.entry_reg_password = Entry(self.registerWindow, width=30)
        self.entry_reg_password.grid(column=1, row=3)

        self.label_reg_confirm_password = Label(self.registerWindow, text='Confirm Password')
        self.label_reg_confirm_password.grid(column=0, row=4)
        self.entry_reg_confirm_password = Entry(self.registerWindow, width=30)
        self.entry_reg_confirm_password.grid(column=1, row=4)

        self.button_reg_register = Button(self.registerWindow, text="회원가입", command=self.register)
        self.button_reg_register.grid(columnspan=2, rowspan=5)

Login().mainloop()