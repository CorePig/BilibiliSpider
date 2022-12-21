# 本文件的作用就是实现用户的身份验证
import time
from tkinter import *
from tkinter import messagebox
import pymysql


class userverify:
    def __init__(self):
        self.flag=False
        #
        # 链接数据库
        # 建立数据库链接（如果不对每一个参数进行赋值可能会报错）
        self.db = pymysql.connect(host='localhost', user='root', password='123456', db='admins')
        # 使用cursor()创建一个游标对象cursor
        self.cirson = self.db.cursor()


        # 初始化登录注册页面
        self.login = Tk()
        self.login.title('Login')
        self.login.geometry('210x150')
        Label(self.login,text='用户登录').grid(row=0,column=0,columnspan=2)
        Label(self.login,text='用户名：').grid(row=1,column=0)
        self.name = Entry(self.login)
        self.name.grid(row=1,column=1)
        Label(self.login,text='密码：').grid(row=2,column=0,sticky=E)
        self.passwd = Entry(self.login,show='*')
        self.passwd.grid(row=2,column=1)
        Button(self.login, text='登录', command=self.successful).grid(row=3, column=0, columnspan=2)
        Button(self.login, text='还没有账号？点我注册！', command=self.registereds).grid(row=4, column=0, columnspan=2)
        self.login.mainloop()
    def selectuser(self,name,passwd):
        self.cirson.execute(f"select * from UserMsg where name='{name}' and passwd='{passwd}';")
        data=self.cirson.fetchall()
        if data:
            return True
        else:
            return False
    def getflag(self):
        return self.flag
    def adduser(self,name,passwd,phone,id):
        self.cirson.execute(f'''insert into UserMsg values('{name}','{passwd}','{phone}',{id});''')
        self.db.commit()
    def successful(self):
        if self.selectuser(self.name.get(),self.passwd.get()):
            messagebox.showinfo(title='successful',message='登录成功')
            self.flag=True
            self.login.destroy()
        else:
            messagebox.showerror(title='wrong',message='登录失败，用户名或密码错误')
    def registereds(self):
        registered = Tk()
        registered.title('registered')
        registered.geometry('230x185')
        Label(registered,text='用户注册').grid(row=0,column=0,columnspan=2)
        Label(registered,text='用户名：').grid(row=1,column=0,sticky=E)
        names = Entry(registered)
        names.grid(row=1,column=1)
        Label(registered,text='密码：').grid(row=2,column=0,sticky=E)
        passwds = Entry(registered,show='*')
        passwds.grid(row=2,column=1)
        Label(registered,text='确认密码：').grid(row=3,column=0)
        repasswd = Entry(registered,show='*')
        repasswd.grid(row=3,column=1)
        Label(registered,text='手机号：').grid(row=4,column=0,sticky=E)
        phonenum = Entry(registered)
        phonenum.grid(row=4,column=1)
        Label(registered,text='身份证号：').grid(row=5,column=0)
        man = Entry(registered)
        man.grid(row=5,column=1)
        def teshufuhao(input_psd):
            string = "~!@#$%^&*()_+-*/<>,.[]\/"
            for i in string:
                if i in input_psd:
                    return True
            return False
        def registeredes():
            if not (any([x.isdigit() for x in names.get()]) and any([x.isalpha() for x in names.get()]) and teshufuhao(names.get())):
                messagebox.showerror(title='wrong',message='注册失败，用户名格式错误，必须包括字母和数字以及特殊符号')
            elif len(passwds.get()) < 8:
                messagebox.showerror(title='wrong',message='注册失败，密码不应少于8位')
            elif passwds.get() != repasswd.get():
                messagebox.showerror(title='wrong',message='注册失败，两次密码不相同')
            elif not (phonenum.get().isdigit() and len(phonenum.get()) == 11):
                messagebox.showerror(title='wrong',message='注册失败，请输入正确的11位手机号')
            elif len(man.get()) != 18:
                messagebox.showerror(title='wrong',message='注册失败，请输入正确的18位身份证号')
            else:
                try:
                    self.adduser(names.get(), passwds.get(), phonenum.get(), man.get())
                    messagebox.showinfo(title='successful',message='注册成功！欢迎您。新会员')
                except Exception as e:
                    print(e)
                    messagebox.showinfo(title='successful',message='信息重复！')



                registered.destroy()
        Button(registered,text='注册',command=registeredes).grid(row=6,column=0,columnspan=2)

if __name__=="__main__":
    UV=userverify()
