# encoding utf-8

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkbs
from ttkbootstrap.constants import *
from PIL import ImageTk, Image
from login_register import login_register       # 导入登入注册模块
from tkinter import messagebox

class item_reservation_system():
    '''物品预约系统'''
    def __init__(self):
        self.root = ttkbs.Window(title='物品预约系统', themename='morph')
        #self.login = login_register(state='login',parents=self.root)
        #self.register = login_register(state='register',parents=self.root)
        self.current_user = None
        self.user_menu = None
        # 变量初始化
        self.ads_image = []   # 广告实例
        self.style()         # 先定义样式
        self.image_loading()        # 加载图片
        self.build_ui()      # 再构建界面
        self.run()

    def image_loading(self):
        '''图片加载'''
        # Beifu School logo
        self.logo = tk.PhotoImage(file='img/xiamen_haicang_beifu_school.png')
        # borrow.png(resize)
        borrow = Image.open('img/ico/borrow.png')
        borrowed = borrow.resize((250,250),Image.LANCZOS)
        self.borrowed = ImageTk.PhotoImage(borrowed)
        # back.png(resize)
        back = Image.open('img/ico/back.png')
        backed = back.resize((250,250),Image.LANCZOS)
        self.backed = ImageTk.PhotoImage(backed)
        # query.png(resize)
        query = Image.open('img/ico/query.png')
        queryed = query.resize((250,250),Image.LANCZOS)
        self.queryed = ImageTk.PhotoImage(queryed)
        # remaining_query.png(resize)
        remaining_query = Image.open('img/ico/remaining_query.png')
        remaining_queryed = remaining_query.resize((250,250),Image.LANCZOS)
        self.remaining_queryed = ImageTk.PhotoImage(remaining_queryed)
        # admin_login.png(resize)
        admin_login = Image.open('img/ico/admin_login.png')
        admin_logined = admin_login.resize((600,250),Image.LANCZOS)
        self.admin_logined = ImageTk.PhotoImage(admin_logined)
        # item_report.png(resize)
        item_report = Image.open('img/ico/item_report.png')
        item_reported = item_report.resize((600,250),Image.LANCZOS)
        self.item_reported = ImageTk.PhotoImage(item_reported)

    def style(self): 
        '''样式设置'''
        self.style_obj = self.root.style

        # 注册样式
        self.style_obj.configure('Login.TButton',
                                 background='green',
                                 font=('楷体', 20))
        self.style_obj.map('Login.TButton',
                           background=[
                               ('active',"#6eaf50"),
                               ('pressed', '#1c7430'),
                           ],
                           foreground=[
                               ('active','#ffffff')
                           ])
        
        # 注册样式
        self.style_obj.configure('Register.TButton',
                                 background="#0400ff",
                                 font=('楷体',20))
        
        # 清除按钮蓝边
        self.style_obj.configure('Cleanblue.TButton',
                                 background='#d9e3f1')
        self.style_obj.map('Cleanblue.TButton',
            background=[
                ('active',"#0067f7"),
                ('pressed',"#d9e3f1")
            ]
        )

        # 个人中心等title样式
        self.style_obj.configure('Title.TLabel',
                                 foreground="#7CB3E0")
        

    def build_ui(self):
        '''构建界面'''
        self.root.attributes('-fullscreen', True)
        
        # top
        self.top_btn_frame = ttkbs.Frame(self.root)
        self.top_btn_frame.pack(side=TOP, padx=20, pady=20, fill='x', anchor='nw')
        
        # logo icon
        self.top_btn_frame_logo_label = ttk.Label(
            self.top_btn_frame,
            image=self.logo
        )
        self.top_btn_frame_logo_label.pack(side=LEFT, pady=10)

        # 按钮frame
        self.top_right_frame = ttkbs.Frame(self.top_btn_frame)
        self.top_right_frame.pack(side=RIGHT)

        # 登录按钮
        self.top_btn_frame_login_btn = ttk.Button(self.top_right_frame,text='登录',style='Login.TButton',width=5,command=self.open_login)
        self.top_btn_frame_login_btn.pack(side=LEFT)

        # 注册按钮
        self.top_btn_frame_register_btn = ttk.Button(self.top_right_frame,text='注册',style='Register.TButton',width=5,command=self.open_register)
        self.top_btn_frame_register_btn.pack(side=LEFT,padx=10)

        # (隐藏)用户菜单按钮  用户名后面会改
        self.user_menu_btn = ttk.Menubutton(self.top_right_frame,text='用户名',style='Login.TButton')

        # 广告位
        self.ads_frame = ttkbs.Frame(self.root,height=350)
        self.ads_frame.pack(pady=10,padx=30,fill='x')
        self.ads_frame.pack_propagate(False)
        # 广告label
        self.ad_label = ttk.Label(self.ads_frame,text='广告正在加载中 请稍后……',font=('楷体',20))
        self.ad_label.pack(expand=True)

        # 按钮frame
        self.btn_frame = ttkbs.Frame(self.root)
        self.btn_frame.pack(expand=True,padx=200,pady=10,fill='both')

        # 配置网格权重，让按钮真正"粘"在左上角 
        self.btn_frame.grid_rowconfigure(0, weight=0)  # 第0行不扩展
        self.btn_frame.grid_rowconfigure(1, weight=0)  # 第1行不扩展
        self.btn_frame.grid_rowconfigure(2,weight=0)    # 第2行不扩展
        self.btn_frame.grid_rowconfigure(3,weight=1)    # 添加一个空列占据剩下空间

        self.btn_frame.grid_columnconfigure(0, weight=0)  # 第0列不扩展
        self.btn_frame.grid_columnconfigure(1,weight=0)     # 第1列不扩展
        self.btn_frame.grid_columnconfigure(2,weight=0)        # 第2列不扩展
        self.btn_frame.grid_columnconfigure(3, weight=1)  # 添加一个空列来占据剩余空间
        
        # "借器材"按钮
        self.btn_frame_borrow = ttk.Button(self.btn_frame,image=self.borrowed,style='Cleanblue.TButton')
        self.btn_frame_borrow.grid(row=0,column=0,sticky=NW)

        # "还器材"按钮
        self.btn_frame_back = ttk.Button(self.btn_frame,image=self.backed,style='Cleanblue.TButton')
        self.btn_frame_back.grid(row=0,column=1,sticky=NW,padx=100)

        # "查询归还状态"按钮
        self.btn_frame_query = ttk.Button(self.btn_frame,style='Cleanblue.TButton',image=self.queryed)
        self.btn_frame_query.grid(row=0,column=2,sticky=NW)

        # "剩余器材查询"按钮
        self.btn_frame_remaining_query = ttk.Button(self.btn_frame,style='Cleanblue.TButton',image=self.remaining_queryed)
        self.btn_frame_remaining_query.grid(row=0,column=3,padx=100,sticky=NW)

        # "管理员登录"按钮
        self.btn_frame_admin_login = ttk.Button(self.btn_frame,image=self.admin_logined,style='Cleanblue.TButton')
        self.btn_frame_admin_login.grid(row=1,column=0,columnspan=2,pady=20)

        # "物品报备、反馈"按钮
        self.btn_frame_item_report = ttk.Button(self.btn_frame,style='Cleanblue.TButton',image=self.item_reported)
        self.btn_frame_item_report.grid(row=1,column=2,columnspan=2,pady=20)

        # 广告加载和显示(放最后)
        self.ads_loading()

    def ads_loading(self):
        '''广告加载函数'''
        image_path = [
            'img/ad_image/ad1.png','img/ad_image/ad2.png','img/ad_image/ad3.png','img/ad_image/ad4.png'
        ]               # 图片存放位置
        ## 1.用for循环加载广告
        # 先用PIL处理图片
        self.ads_imagephotoed = []           # 生成实例列表
        for i, filename in enumerate(image_path):
            img = Image.open(filename)
            img_resized = img.resize((1600,360),Image.LANCZOS)

            photo = ImageTk.PhotoImage(img_resized)
            self.ads_imagephotoed.append(photo)

        ## 2.添加到组件(要用到新的函数)
        self.current_ad = 0
        self.adds_ads_label()

    def adds_ads_label(self):
        '''将广告添加到组件'''
        self.current_ad = (self.current_ad  + 1) % len(self.ads_imagephotoed)
        self.ad_label.config(image=self.ads_imagephotoed[self.current_ad])
        self.ad_label.after(3000,self.adds_ads_label)               # 运用after函数

    def open_login(self):
        login_window = login_register(self,'login')
        login_window.state_yes_no()
        login_window.show()

    def open_register(self):
        register_window = login_register(self,'register')
        register_window.state_yes_no()
        register_window.show()

    def update_login_status(self):
        '''更新页面(更改下拉框)(由login_register.py调用)'''
        if self.current_user:
            print(f'登录成功!{self.current_user['name']}')

            # 隐藏登录 注册 按钮
            self.top_btn_frame_login_btn.pack_forget()
            self.top_btn_frame_register_btn.pack_forget()

            # 更改用户菜单按钮文字
            self.user_menu_btn.config(text=f'👤 {self.current_user['name']}')

            # 创建下拉菜单
            self.create_user_menu()

            # 显示用户菜单按钮
            self.user_menu_btn.pack(side=LEFT)

        else:
            messagebox.showerror(title='登录',message='登录状态更新失败',parent=self.root)

    def create_user_menu(self):
        '''创建用户下拉菜单'''
        if self.user_menu is None:
            self.user_menu = tk.Menu(self.user_menu_btn,tearoff=0,background="#3CFF01",font=('等线',15),activebackground="#63ce63",borderwidth=5)
            self.user_menu_btn.config(menu=self.user_menu)

        # 清空旧菜单
        self.user_menu.delete(0,tk.END)

        # 添加菜单项
        # 1. 用户名 (不可点击)
        self.user_menu.add_command(label=f'👤 {self.current_user['name']}',state='disabled')
        self.user_menu.add_separator()

        # 2. 个人中心
        self.user_menu.add_command(label='📋 个人中心',command=self.show_user_profile)

        # 3. 我的预约
        self.user_menu.add_command(label='📅 我的预约')

        # 4. 退出登录
        self.user_menu.add_command(label='🚪 退出登录')

    def show_user_profile(self):
        '''个人中心command'''
        root = ttkbs.Toplevel(self.root)
        root.title('个人中心')
        root.geometry('650x550')
        root.resizable(False,False)
        root.attributes('-topmost', True)
        root.grab_set()

        # 显示标题
        ttk.Label(root,text='个人中心',font=('等线',25),style='Title.TLabel').pack(side=TOP,fill='y',pady=20)

        # 显示控件
        

    def run(self):
        self.root.mainloop()

app = item_reservation_system()