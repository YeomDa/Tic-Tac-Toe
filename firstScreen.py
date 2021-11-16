from tkinter import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate("firebase/opensw-team1-firebase-adminsdk-ln99u-734bf11a84.json")
default_app = firebase_admin.initialize_app(cred)

class Login() :
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title('Login & Register')
        self.window.geometry('300x100')

        self.label_info = Label(self.window, text='로그인', font=('돋음', 10))
        self.label_info.grid(column = 0, row = 0)

        self.label_email = Label(self.window, text='Email', font=('돋음', 10))
        self.label_email.grid(column = 0, row = 1)
        self.entry_email = Entry(self.window, width = 30)
        self.entry_email.grid(column = 1, row = 1)

        self.label_pwd = Label(self.window, text='PW', font=('돋음', 10)) 
        self.label_pwd.grid(column = 0, row = 2)
        self.entry_pwd = Entry(self.window, width = 30)
        self.entry_pwd.grid(column = 1, row = 2)

        self.label_nickname = Label(self.window, text='Nickname', font=('돋음', 10)) 
        self.label_nickname.grid(column = 0, row = 3)
        self.entry_nickname = Entry(self.window, width = 30)
        self.entry_nickname.grid(column = 1, row = 3)

        self.button_login = Button(self.window, text='로그인', bg='blue', fg='white', command=self.login)
        self.button_login.grid(column = 0, row = 4)
        self.button_register = Button(self.window, text='회원가입', bg='blue', fg='white', command=self.register)
        self.button_register.grid(column = 1, row = 4)

    def mainloop(self) :
        self.window.mainloop()

    def login(self) :
        print('로그인 버튼 클릭')
        input_email = self.entry_email.get()

        if(len(input_email) == 0) :
            print('이메일을 입력해주세요.')
        else :
            print('해당 이메일로 가입된 사용자의 정보를 출력합니다.')
            user = auth.get_user_by_email(input_email)
            print('이메일 :', user.email)
            print('UID :', user.uid)
            print('닉네임 :', user.display_name)
        

    def register(self) :
        print('회원가입 버튼 클릭')
        input_email = self.entry_email.get()
        input_pwd = self.entry_pwd.get()
        input_nickname = self.entry_nickname.get()

        if(len(input_email) == 0 or len(input_pwd) == 0 or len(input_nickname) == 0) :
            print('모든 입력창에 정보를 입력해주세요.')
        else :
            user = auth.create_user(email=input_email, password=input_pwd, display_name=input_nickname)
            print('회원가입이 완료되었습니다.')
            print('이메일 :', user.email)
            print('UID :', user.uid)
            print('닉네임 :', user.display_name)

Login().mainloop()