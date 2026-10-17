# encoding utf-8
# 程序为jsh编写 盗版必究！ ©2026 jsh 
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkbs
from ttkbootstrap.constants import *
from PIL import ImageTk, Image
import json
from tkinter import messagebox
import pymysql as mysql
from ttkbootstrap.widgets.scrolled import ScrolledText
import re 
import dns.resolver
# smtp 模块
import smtplib 
from email.mime.text import MIMEText
import secrets
import string
import hashlib

class login_register():
    def __init__(self,parents,state):
        self.parents = parents
        self.login_register_open = False
        self.state = state
        self.login_pwd_show_img = True       # 判断pwd图片     true为no_password_show   false为password_show
        self.register_pwd_show_img = True   # 判断pwd图片     true为no_password_show   false为password_show
        self.smtp_host = 'smtp.163.com'              # smtp服务端
        self.mail_user = 'jsh20140506@163.com'       # smtp发送用户端
        self.mail_port = 587                         # smtp端口
        self.smtp_code = 'NQv48iNpM4KDm5Sh'          # smtp授权码
        # 倒计时相关变量
        self.left_time = 0          # 整个文件的剩余倒计时，关闭弹窗也不清零
        self.time_id = None         # 计时器id
        self.email_re = r'^[a-zA-Z0-9_\-+.]+@.*$'
        self.email_check_bool = False           # 判断邮箱是否有效变量
    def style(self):
        '''样式style'''
        self.style_obj = self.root.style

        ## 样式
        # 登录、注册样式
        self.style_obj.configure('Lore.TLabel',
                                 foreground="#409C34",
                                 font=('楷体', 20))
        # 用户名、密码显示样式
        self.style_obj.configure('Login_register.TLabel',
                                 foreground="#6d92f7",
                                 font=('仿宋',15))
        # 用户名、密码输入框样式
        self.style_obj.configure('login_register.TEntry',
                                 foreground="#000000",
                                 background="#60eb9a",
                                 font=('楷体',15))
        # 登录按钮样式
        self.style_obj.configure('login_btn.TButton',
                                 background="#25667a",
                                 foreground="#ffffff",
                                 font=('方正舒体',15))
        self.style_obj.map('login_btn.TButton',
                           background=[
                               ('active',"#6fb2da"),
                               ('pressed', '#25667a')
                           ],
                           foreground=[
                               ('active','#ffffff')
                           ])
        # StringVar样式
        self.style_obj.configure('stringvar.TLabel',
                                 foreground="#ff0000",
                                 font=('宋体',15)
                                 )
        
        # 1. Notebook 容器样式
        self.style_obj.configure('Custom.TNotebook',
                                background='#ffffff',
                                borderwidth=0,
                                tabmargins=[0, 0, 0, 0])  # 移除标签边距
    
        # 2. Notebook 标签样式 - 必须同时配置所有状态
        self.style_obj.configure('Custom.TNotebook.Tab',
                                font=('楷体', 14, 'bold'),
                                foreground='#409C34',
                                padding=[110, 20],
                                background='#f0f8f0',
                                borderwidth=0,
                                focuscolor='none',
                                width=15)  # 移除焦点边框
    
        # 3. 关键：使用 map 配置所有状态，覆盖主题默认
        self.style_obj.map('Custom.TNotebook.Tab',
                          # 前景色
                          foreground=[('selected', '#06722a'),      # 选中：深绿色
                                     ('active', '#409C34'),         # 悬停：绿色
                                     ('!selected', '#409C34')],     # 未选中：绿色
                        # 背景色
                        background=[('selected', '#e8f5e9'),      # 选中：浅绿色
                                     ('active', '#d4edda'),         # 悬停：更浅的绿色
                                     ('!selected', '#f5f5f5')],     # 未选中：浅灰色
                        # 字体
                        font=[('selected', ('楷体', 14, 'bold')),
                              ('!selected', ('楷体', 14, 'bold'))],
                        # 内边距
                        padding=[('selected', [110, 20]),
                                 ('!selected', [110, 20])])
        
        # 取消按钮style
        self.style_obj.configure('exit.TButton',
                                 font=('微软雅黑',15),
                                 background="#e44a4a")
        
        # 确认按钮
        self.style_obj.configure('cheak.TButton',
                                 font=('微软雅黑',15),
                                 background="#5bdd66")
        
    def photo_image_file(self):
        '''image实例化加载'''
        # 处理password_show图片
        password_show = Image.open('img/password/password_show.png')
        password_showed = password_show.resize((30,30),Image.LANCZOS)
        self.img_password_show = ImageTk.PhotoImage(password_showed)
        # 处理no_password_show图片
        no_password_show = Image.open('img/password/no_password_show.png')
        no_password_showed = no_password_show.resize((30,30),Image.LANCZOS)
        self.img_no_password_show = ImageTk.PhotoImage(no_password_showed)

    def state_yes_no(self):
        '''根据state判断变量'''
        if self.state == 'login':
            self.title = '登录'

        elif self.state == 'register':
            self.title = '注册'

    def show(self):
        '''展示登录界面UI'''
        if self.login_register_open == True:        
            self.root.lift()
            self.root.focus_force()
            return
        
        self.root = ttkbs.Toplevel(self.parents)
        self.login_register_open = True
        self.root.geometry('1000x900')
        self.root.title(self.title)
        self.root.protocol("WM_DELETE_WINDOW",self.on_login_close)
        self.root.grab_set()  # 捕获所有事件
        self.root.focus_set()  # 设置焦点
        self.root.attributes('-topmost', True)  # 置顶
        self.root.pack_propagate(False)
        self.style()
        self.photo_image_file()
        # 关闭、初始化计时器
        self.left_time = 0
        if self.time_id is not None :
            self.root.after_cancel(self.time_id)
            self.time_id = None

        # 注册/登录Label
        self.title_label = ttk.Label(self.root,text=self.title,font=('仿宋',30),style='Lore.TLabel').pack(pady=30)
        # 其他组件处理
        self.other_component = ttkbs.Frame(self.root,height=500)
        self.other_component.pack(expand=True,padx=20,pady=20,fill='both')
        #notebook切换
        self.login_register_notebook = ttk.Notebook(self.other_component,style='Custom.TNotebook',height=700)
        self.login_register_notebook.pack(expand=True,fill='both')
        ## 生成子选项卡(登录)
        self.login_notebook_tab1 = ttkbs.Frame(self.login_register_notebook)
        # 登录提示
        self.login_notebook_tab1_titlelab = ttk.Label(self.login_notebook_tab1,text='登录',style='Lore.TLabel')
        self.login_notebook_tab1_titlelab.pack()
        # 输入框等（grid）
        self.login_notebook_tab1_ety_btn = ttkbs.Frame(self.login_notebook_tab1)
        self.login_notebook_tab1_ety_btn.pack(expand=True,fill='both',padx=40,pady=10)
        # 输入框(用户名)(提示)
        self.login_notebook_tab1_username_lab = ttk.Label(self.login_notebook_tab1_ety_btn,text='用户名(邮箱登录请填邮箱):',style='Login_register.TLabel')
        self.login_notebook_tab1_username_lab.grid(row=0,column=0,sticky='nw')
        # 输入框(用户名)(输入框)
        self.login_notebook_tab1_username_ety = ttk.Entry(self.login_notebook_tab1_ety_btn,style='login_register.TEntry',width=50)
        self.login_notebook_tab1_username_ety.grid(row=1,column=0,sticky='nw',pady=10)
        # 输入框(密码)(提示)
        self.login_notebook_tab1_pwd_lab = ttk.Label(self.login_notebook_tab1_ety_btn,text='密码:',style='Login_register.TLabel')
        self.login_notebook_tab1_pwd_lab.grid(row=2,column=0,sticky='w',pady=10)
        # 输入框(密码)(输入框)
        self.login_notebook_tab1_pwd_ety = ttk.Entry(self.login_notebook_tab1_ety_btn,style='login_register.TEntry',width=50,show='*')
        self.login_notebook_tab1_pwd_ety.grid(row=3,column=0,sticky='w',pady=10)
        # 显示密码按钮
        self.login_notebook_tab1_pwd_btn = ttkbs.Button(self.login_notebook_tab1_ety_btn,style='outline',command=self.login_pwd_show_img_command,image=self.img_no_password_show)
        self.login_notebook_tab1_pwd_btn.grid(row=3,column=1)
        # 密码错误的StringVar
        self.login_notebook_tab1_stringvar = tk.StringVar()
        self.login_notebook_tab1_stringvar_label = ttk.Label(self.login_notebook_tab1_ety_btn,textvariable=self.login_notebook_tab1_stringvar,style='stringvar.TLabel')
        self.login_notebook_tab1_stringvar_label.grid(row=4,column=0,columnspan=2,pady=10)
        # 确认登录按钮
        self.login_notebook_tab1_cheak_btn = ttk.Button(self.login_notebook_tab1_ety_btn,text='登录',style='login_btn.TButton',command=self.login_check_btn_command)
        self.login_notebook_tab1_cheak_btn.grid(row=5,column=0,columnspan=1,pady=10)

        ## 生成子选项卡(注册)
        self.register_notebook_tab2 = ttkbs.Frame(self.login_register_notebook)
        #注册提示
        self.register_notebook_tab2_titlelab = ttk.Label(self.register_notebook_tab2,text='注册',style='Lore.TLabel')
        self.register_notebook_tab2_titlelab.pack()
        # 用户名等组件Frame
        self.register_notebook_tab2_ety_frame = ttk.Frame(self.register_notebook_tab2)
        self.register_notebook_tab2_ety_frame.pack(fill='both',expand=True,padx=40,pady=10)
        # 输入用户名提示
        self.register_notebook_tab2_user_lab = ttk.Label(self.register_notebook_tab2_ety_frame,text='请输入用户名(可用此用户名进行登录):',style='Login_register.TLabel')
        self.register_notebook_tab2_user_lab.grid(row=0,column=0,sticky='nw')
        # 输入用户名ety
        self.register_notebook_tab2_user_ety = ttk.Entry(self.register_notebook_tab2_ety_frame,style='login_register.TEntry',width=50)
        self.register_notebook_tab2_user_ety.grid(row=1,column=0,sticky='nw',pady=5)
        # 输入邮箱lab
        self.register_notebook_tab2_email_lab = ttk.Label(self.register_notebook_tab2_ety_frame,text='请填入自己的邮箱:',style='Login_register.TLabel')
        self.register_notebook_tab2_email_lab.grid(row=2,column=0,pady=5,sticky='nw')
        # 邮箱ety
        self.register_notebook_tab2_email_ety = ttk.Entry(self.register_notebook_tab2_ety_frame,width=50)
        self.register_notebook_tab2_email_ety.grid(row=3,column=0,pady=5,sticky='nw')
        # 邮箱验证btn
        self.register_notebook_tab2_email_btn = ttk.Button(self.register_notebook_tab2_ety_frame,text='点我验证邮箱',command=self.register_smtp_sevice,style='login_btn.TButton')
        self.register_notebook_tab2_email_btn.grid(row=3,column=1,sticky='nw',padx=5)            # 这里采用弹窗办法，点按钮后弹出一个界面，输入完后就可以进
        # 密码lab
        self.register_notebook_tab2_psw_lab = ttk.Label(self.register_notebook_tab2_ety_frame,text='请输入设定密码：',style='Login_register.TLabel')
        self.register_notebook_tab2_psw_lab.grid(row=4,column=0,pady=5,sticky='nw')
        # 密码ety
        self.register_notebook_tab2_psw_ety = ttk.Entry(self.register_notebook_tab2_ety_frame,width=50,show='*')
        self.register_notebook_tab2_psw_ety.grid(row=5,column=0,pady=5,sticky='nw')
        # 小眼睛btn
        self.register_notebook_tab2_psw_btn = ttkbs.Button(self.register_notebook_tab2_ety_frame,style='outline',command=self.register_pwd_show_img_command,image=self.img_no_password_show)
        self.register_notebook_tab2_psw_btn.grid(row=5,column=1,sticky='nw',padx=5)
        # 确认密码lab
        self.register_notebook_tab2_cheakpsw_lab = ttk.Label(self.register_notebook_tab2_ety_frame,text='请再输一遍密码，以确认:',style='Login_register.TLabel')
        self.register_notebook_tab2_cheakpsw_lab.grid(row=6,column=0,sticky='nw',pady=5)
        # 确认密码ety
        self.register_notebook_tab2_cheakpsw_ety = ttk.Entry(self.register_notebook_tab2_ety_frame,show='*',width=50)
        self.register_notebook_tab2_cheakpsw_ety.grid(row=7,column=0,sticky='nw',pady=5)
        # StringVar错误报告
        self.register_notebook_tab2_stringvar = tk.StringVar()
        # SV组件
        self.register_notebook_tab2_stringvar_lab = ttk.Label(self.register_notebook_tab2_ety_frame,textvariable=self.register_notebook_tab2_stringvar,style='danger.TLabel',font=('楷体',15))
        self.register_notebook_tab2_stringvar_lab.grid(row=7,column=2,sticky='ew')
        # 注册按钮
        self.register_notebook_tab2_register_btn = ttk.Button(self.register_notebook_tab2_ety_frame,text='注册',style='login_btn.TButton',command=self.register_check_btn_command)
        self.register_notebook_tab2_register_btn.grid(row=8,column=0,columnspan=2,pady=5)

        # 添加选项卡
        self.login_register_notebook.add(self.login_notebook_tab1,text='登录')
        self.login_register_notebook.add(self.register_notebook_tab2,text='注册')
        # 判断登录/注册页
        if self.state == 'login':
            self.login_register_notebook.select(0)
        elif self.state == 'register':
            self.login_register_notebook.select(1)
        else:
            messagebox.showerror('self.state信息传入错误!请检查代码后重试!','错误',parent=self.root)

        self.login_register_open = True

    def login_check_btn_command(self):
        '''登录按钮command'''
        password = self.login_notebook_tab1_pwd_ety.get().strip()
        name = self.login_notebook_tab1_username_ety.get().strip()
        if password == '':
            messagebox.showwarning(title='警告',message='密码为空!请检查后重试!',parent=self.root)
            return
        if name == '':
            messagebox.showwarning(title='警告',message='用户名为空!请检查后重试!',parent=self.root)
            return
        # 检测密码是否为中文 或 非法字符
        illegal_chars = re.findall(r'[^A-Za-z0-9_]', password)
        if illegal_chars:
            messagebox.showwarning(title='警告',message='密码中包含非法字符！请检查后重试！',parent=self.root)
            return
        # 判断用户名输入框是否为邮箱
        is_email = '@' in name
        ## 连接mysql
        # 清空连接
        conn = None
        cursor = None
        # 尝试连接mysql
        try:
            conn = mysql.connect(
                host='127.0.0.1',
                port=7777,
                user='root',
                password='Jsh123456',
                database='reserve_system',
                charset='utf8'
            )
            cursor = conn.cursor()
            # 根据用户名与邮箱是否查询内容
            if is_email:
                sql = 'SELECT `id`,`name`,`email`,`password` FROM `users` WHERE `email` = %s'
                cursor.execute(sql,args=(name,))
            else:
                sql = 'SELECT `id`,`name`,`email`,`password` FROM `users` WHERE `name` = %s'
                cursor.execute(sql,args=(name,))
            # 获取数据
            result = cursor.fetchone()
            ## 判断账户是否存在
            if result is None:
                messagebox.showwarning(title='登录失败',message='用户或密码输入错误，请检查后重试!',parent=self.root)
                return
            # 存储数据
            user_id, user_name, user_email, user_password = result

            # 验证密码
            if password != user_password:
                messagebox.showwarning(title='登录失败',message='用户或密码输入错误，请检查后重试!',parent=self.root)
                return
            # 登录成功
            # 传回用户信息
            self.parents.current_user = {
                'id': user_id,
                'name': user_name,
                'email': user_email,
                'password': user_password
            }
            self.current_user = {
                'id': user_id,
                'name': user_name,
                'email': user_email,
                'password': user_password                
            }

            # 调用index.py的update_login_status 方法
            self.parents.update_login_status()

            # 弹窗
            messagebox.showinfo(title='登录成功',message=f'账户 {self.current_user['name']} 登录成功!',parent=self.root)

            # 关闭窗口
            self.on_login_close()

        except Exception as e:
            messagebox.showerror(title='错误',message=e,parent=self.root)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def register_check_btn_command(self):
        '''注册按钮command'''
        # 先判断是否有值为空
        user_name = self.register_notebook_tab2_user_ety.get().strip()
        if user_name == '':
            messagebox.showwarning(title='警告',message='请输入用户名！',parent=self.root)
            return
        
        pwd = self.register_notebook_tab2_psw_ety.get().strip()
        if pwd == '':
            messagebox.showwarning(title='警告',message='请输入密码！',parent=self.root)
            return
        
        check_pwd = self.register_notebook_tab2_cheakpsw_ety.get().strip()
        if check_pwd == '':
            messagebox.showwarning(title='警告',message='请输入确认密码！',parent=self.root)
            return
        if self.email_check_bool == False:
            messagebox.showwarning(title='警告',message='请确认邮箱！',parent=self.root)
            return
        if check_pwd != pwd:
            messagebox.showwarning(title='警告',message='确认密码与密码不一致！',parent=self.root)
            return
        # \u4e00-\u9fa5 是中文字符的 Unicode 范围
        illegal_chars = re.findall(r'[^A-Za-z0-9_]', pwd)
        if illegal_chars:
            messagebox.showwarning(title='警告',message='密码中包含非法字符！请检查后重试！',parent=self.root)
            return
        illegal_username = re.findall(r'[^A-Za-z0-9_\u4e00-\u9fa5]', user_name)
        if illegal_username:
            unique_illegal = ' '.join(set(illegal_username))
            messagebox.showwarning(
                title='用户名包含非法字符',
                message=f'用户名只能包含字母、数字、中文和下划线\n\n检测到非法字符：{unique_illegal}',
                parent=self.root
            )
            return
        email = self.register_notebook_tab2_email_ety.get().strip()
        ## 先检查本用户名是否已经注册(防SQL注入)
        # 连接
        conn = mysql.connect(host='127.0.0.1',user='root',password='Jsh123456',database='reserve_system',charset='utf8',port=7777)
        try:
            cursor = conn.cursor()
            # 1.判断该用户名是否已经使用
            cursor.execute('SELECT EXISTS(SELECT 1 FROM `users` WHERE `name` = %s) AS `exists`',args=(user_name,))
            name_exists = bool(cursor.fetchone()[0])
            if name_exists:
                messagebox.showwarning(title='提醒',message='您注册的用户名已被占用！请更改用户名后重试!',parent=self.root)
                return
            # 2.判断该邮箱是否使用
            cursor.execute('SELECT EXISTS(SELECT 1 FROM `users` WHERE `email` = %s) AS `exists`',args=(email,))
            email_exists = bool(cursor.fetchone()[0])
            if email_exists:
                messagebox.showwarning(title='提醒',message='您注册的邮箱已被占用！请更改邮箱后重试!',parent=self.root)
                return
            # 存入数据
            cursor.execute('INSERT INTO `users` (`name`,`email`,`password`) VALUES (%s, %s, %s)',args=(user_name,email,check_pwd))
            conn.commit()   # 提交事务
            messagebox.showinfo(title='成功！',message='用户注册成功!请到 登录 选项卡进行登录！',parent=self.root)
            self.login_register_notebook.select(0)
        except Exception as e:
            conn.rollback()
            messagebox.showerror(title='注册失败！',message=f'注册失败！错误{e},请找工程师修复！',parent=self.root)
        finally:
            cursor.close()
            conn.close()

    def register_agree_see(self,name):
        '''展示协议内容'''
        if name == 'user_agree':
            self.user_agree_window = ttkbs.Toplevel(self.cheak_smtp_window)
            self.user_agree_window.title('用户协议')
            self.user_agree_window.transient(self.cheak_smtp_window)
            self.user_agree_window.grab_set()
            self.user_agree_window.focus_set()
            self.user_agree_window.geometry('800x800')
            self.user_agree_window_scrolltext = ScrolledText(self.user_agree_window,font=('楷体',15),hbar=True,autohide=False)
            self.user_agree_window_scrolltext.pack(expand=True,fill='both')
            # 提取字符
            with open('agree/user_agree.txt',encoding='utf-8',mode='r') as f:
                self.user_agree_window_user_agree = f.read()
                    # 先允许写入
            self.user_agree_window_scrolltext.text.config(state=NORMAL)
            self.user_agree_window_scrolltext.insert(END,self.user_agree_window_user_agree)
            # 写入完成后锁定，禁止编辑
            self.user_agree_window_scrolltext.text.config(state=DISABLED)
            # 滚动到顶部
            self.user_agree_window_scrolltext.see("1.0")
        
        if name == 'rules':
            self.rules_window = ttkbs.Toplevel(self.cheak_smtp_window)
            self.rules_window.title('使用规则 规范')
            self.rules_window.transient(self.cheak_smtp_window)
            self.rules_window.grab_set()
            self.rules_window.focus_set()
            self.rules_window.geometry('800x800')
            self.rules_window_scrolltext = ScrolledText(self.rules_window,font=('楷体',15),hbar=True,autohide=False)
            self.rules_window_scrolltext.pack(expand=True,fill='both')
            with open('agree/rules.txt',encoding='utf-8',mode='r') as s:
                self.rules_window_scrolltext.text.config(state=NORMAL)
                self.rules_window_scrolltext.insert(END,s.read())
                self.rules_window_scrolltext.text.config(state=DISABLED)
            self.rules_window_scrolltext.see('1.0')

    def smtp_send_command(self):
        '''发送验证码按钮command'''
        # 获取邮箱数据
        email = self.register_notebook_tab2_email_ety.get().strip()
        # 匹配邮箱(包含空白匹配)
        email_reg = re.fullmatch(self.email_re,email)
        if email_reg == None:
            messagebox.showwarning(title='提示',message='邮箱格式不正确！请检查！',parent=self.cheak_smtp_window)
            return
        # 分割域名
        _, domain = email.split('@',1)
        # 判断域名
        try:
            # 查询mx记录
            dns.resolver.resolve(domain,'MX')
        except dns.resolver.NXDOMAIN:
            # 域名不存在
            messagebox.showwarning(title='注意',message='当前域名不存在！请检查邮箱后重试！',parent=self.cheak_smtp_window)
            return
        except dns.resolver.NoAnswer:
            messagebox.showwarning(title='注意',message='当前域名存在 但是没有邮箱服务器！请检查重试',parent=self.cheak_smtp_window)
            return
        except Exception as e:
            messagebox.showerror(title='报错',message=f'{e}',parent=self.cheak_smtp_window)
            return
        
        # 检测复选框是否勾选
        if self.cheak_smtp_window_agree_var.get() == False:
            messagebox.showwarning(title='警告⚠',message='您未勾选复选框 请勾选复选框后重新发送！',parent=self.cheak_smtp_window)
            return
        
        # 发送验证码
        receivars = [self.register_notebook_tab2_email_ety.get()]
        # 验证码6字随机
        self.email_code = ''.join(secrets.choice(string.digits) for _ in range(6))
        # 发送文本
        msg = f'''
            尊敬的女士/先生：
            您好！

            这里是公共物品借阅系统，您正在注册本程序，您的隐私、密码将会被我们妥善处理，所以您不用担心。
        您正在注册环节中的验证邮箱，您的验证码为：{self.email_code}。
        请您妥善保管验证码，不要将验证码告诉给陌生人。本验证码生效时间：本次发送
        请您将数字填写到系统当中，数字间不要留空白，谢谢您的配合！
        若您没有操作注册,那请忽略本条邮件，有可能是有人正在注册,填错了邮箱。

        祝    
        注册顺利！


                                                                公共物品预约系统管理/编写团队
        '''
        title = '公共物品预约系统 验证码'
        message = MIMEText(msg,'plain','utf8')
        # 发送邮件
        # 邮件发送者
        message['From'] = '{}'.format(self.mail_user)
        # 邮件接收者
        message['To'] = ','.join(receivars)
        # 设置标题
        message['Subject'] = title
        # 连接账户 登录服务
        server = smtplib.SMTP_SSL(self.smtp_host,self.mail_port)
        server.login(self.mail_user,self.smtp_code)
        # 发送邮件
        server.sendmail(self.mail_user,receivars,message.as_string())
        server.quit()
        messagebox.showinfo(title='提示',message='验证码已发送!请及时查看邮箱并填写到验证码栏!若未收到,请查看垃圾邮件或重新发送!',parent=self.cheak_smtp_window)
        ## 倒计时程序
        # 开启倒计时(60s)
        self.left_time = 60
        self.cheak_smtp_window_sendcode_btn.config(state=DISABLED,text=f'发送验证码({self.left_time}s)')
        # 启动定时器
        if self.time_id is not None:
            self.root.after_cancel(self.time_id)
        self.count_down_timer()

    def count_down_timer(self):
        '''开始倒计时参数'''
        # 倒计时结束判断
        if self.left_time <= 0:
            self.left_time = 0
            self.time_id = None
            # 如果弹窗还在，恢复 按钮状态
            if hasattr(self,'cheak_smtp_window') and self.cheak_smtp_window.winfo_exists():
                self.cheak_smtp_window_sendcode_btn.config(state=NORMAL,text='发送验证码')
            return
        # self.left_time 减1
        self.left_time -= 1
        # 如果弹窗还在，更新弹窗文字
        if hasattr(self,'cheak_smtp_window') and self.cheak_smtp_window.winfo_exists():
            self.cheak_smtp_window_sendcode_btn.config(text=f'发送验证码({self.left_time}s)')
        # 减少秒数，挂载root窗口
        self.time_id = self.root.after(1000,self.count_down_timer)

    def register_smtp_sevice(self):
        '''“验证邮箱”btn command'''
        # 弹出验证窗口
        self.cheak_smtp_window = ttkbs.Toplevel()
        # 更改title
        self.cheak_smtp_window.title('邮箱验证')
        # 设置大小
        self.cheak_smtp_window.geometry('800x600')
        # 设置窗口置顶
        self.cheak_smtp_window.attributes('-topmost', True)
        self.cheak_smtp_window.transient(self.root)
        self.cheak_smtp_window.grab_set()
        self.cheak_smtp_window.focus_set()
        # 设置窗口不可调整大小
        self.cheak_smtp_window.resizable(False,False)
        # 设置窗口组件
        # title
        ttk.Label(self.cheak_smtp_window,text='邮箱验证',font=('楷体',30),style='Lore.TLabel').pack(pady=30)
        # 发送验证码btn
        self.cheak_smtp_window_sendcode_btn = ttk.Button(self.cheak_smtp_window,text='发送验证码',style='login_btn.TButton',command=self.smtp_send_command)
        self.cheak_smtp_window_sendcode_btn.pack(pady=10)
        # 验证码输入提示
        self.cheak_smtp_window_code_lab = ttk.Label(self.cheak_smtp_window,text='请输入验证码:',style='Login_register.TLabel')
        self.cheak_smtp_window_code_lab.pack(pady=10)
        # 验证码输入框
        self.cheak_smtp_window_code_ety = ttk.Entry(self.cheak_smtp_window,width=50)
        self.cheak_smtp_window_code_ety.pack(pady=10)
        ## 协议同意单选框
        # 链接btn与checkbtn的frame
        self.cheak_smtp_window_agree_frame = ttkbs.Frame(self.cheak_smtp_window)
        self.cheak_smtp_window_agree_frame.pack(fill='x',pady=8,padx=90)
        # boolvar 查询数据
        self.cheak_smtp_window_agree_var = tk.BooleanVar()
        self.cheak_smtp_window_agree_cheakbtn = ttkbs.Checkbutton(self.cheak_smtp_window_agree_frame,variable=self.cheak_smtp_window_agree_var,onvalue=True,offvalue=False)
        self.cheak_smtp_window_agree_cheakbtn.grid(row=0,column=0,padx=5)
        # 协议ui
        ttk.Label(self.cheak_smtp_window_agree_frame,text='请您仔细查看').grid(row=0,column=1,padx=5)
        self.cheak_smtp_window_agree_user_btn = ttkbs.Button(self.cheak_smtp_window_agree_frame,text='用户协议',style='link',cursor='hand2',command=lambda:self.register_agree_see(name='user_agree'))
        self.cheak_smtp_window_agree_user_btn.grid(row=0,column=2)
        ttk.Label(self.cheak_smtp_window_agree_frame,text='与').grid(row=0,column=3)
        self.cheak_smtp_window_agree_rules_btn = ttkbs.Button(self.cheak_smtp_window_agree_frame,text='软件使用规范',style='link',cursor='hand2',command=lambda:self.register_agree_see(name='rules'))
        self.cheak_smtp_window_agree_rules_btn.grid(row=0,column=4)        
        ttk.Label(self.cheak_smtp_window_agree_frame,text='后打勾以继续注册').grid(row=0,column=5)
        # 取消 确认 按钮
        self.cheak_smtp_window_btn_frame = ttk.Frame(self.cheak_smtp_window)
        self.cheak_smtp_window_btn_frame.pack(expand=True,pady=10,padx=10)
        self.cheak_smtp_window_exit_btn = ttk.Button(self.cheak_smtp_window_btn_frame,text='取消',style='exit.TButton',command=lambda:self.cheak_smtp_window.destroy())
        self.cheak_smtp_window_exit_btn.grid(row=0,column=0,padx=5)
        self.cheak_smtp_window_cheak_btn = ttk.Button(self.cheak_smtp_window_btn_frame,text='确认',style='cheak.TButton',command=self.cheak_smtp_window_command)
        self.cheak_smtp_window_cheak_btn.grid(row=0,column=1)
        ## 倒计时模块
        # 打开弹窗同步倒计时状态
        if self.left_time > 0:
            self.cheak_smtp_window_sendcode_btn.config(state=DISABLED,text=f'发送验证码({self.left_time})')
        else:
            self.cheak_smtp_window_sendcode_btn.config(state=NORMAL,text='发送验证码')

        # 窗口关闭
        self.cheak_smtp_window.protocol("WM_DELETE_WINDOW", lambda: self.cheak_smtp_window.destroy())
        
    def cheak_smtp_window_command(self):
        '''确认邮箱 确认键command'''
        # 获取单选框值
        cheakbtn_value = self.cheak_smtp_window_agree_var.get()
        # 获取用户写入数字
        ety_value = self.cheak_smtp_window_code_ety.get().strip()
        # 比较用户输入数值是否一致
        if ety_value == str(self.email_code) and cheakbtn_value == True :
            self.register_notebook_tab2_email_btn.config(text='验证成功！可继续操作！',state=DISABLED)
            self.register_notebook_tab2_email_ety.config(state=DISABLED)
            self.email_check_bool = True
            messagebox.showinfo(title='正确',message='邮箱6字效验码正确!可进行下一步注册！',parent=self.cheak_smtp_window)
            self.cheak_smtp_window.destroy()
            return
        else:
            messagebox.showwarning(title='错误',message='您输入的数值错误，请重新输入后提交！',parent=self.cheak_smtp_window)
            return

    def register_pwd_show_img_command(self):
        '''注册页密码切换显示'''
        if self.register_pwd_show_img == True :
            self.register_notebook_tab2_psw_ety.config(show='')
            self.register_notebook_tab2_cheakpsw_ety.config(show='')
            self.register_notebook_tab2_psw_btn.config(image=self.img_password_show)
            self.register_pwd_show_img = False

        else:
            self.register_notebook_tab2_psw_ety.config(show='*')
            self.register_notebook_tab2_cheakpsw_ety.config(show='*')
            self.register_notebook_tab2_psw_btn.config(image=self.img_no_password_show)
            self.register_pwd_show_img = True

    def login_pwd_show_img_command(self):
        '''登录页密码切换显示'''
        if self.login_pwd_show_img == True :
            self.login_notebook_tab1_pwd_ety.config(show='')
            self.login_notebook_tab1_pwd_btn.config(image=self.img_password_show)
            self.login_pwd_show_img = False

        else:
            self.login_notebook_tab1_pwd_ety.config(show='*')
            self.login_notebook_tab1_pwd_btn.config(image=self.img_no_password_show)
            self.login_pwd_show_img = True
    
    def on_login_close(self):
        '''更改self.login_register_open'''
        # 取消定时器
        if self.time_id is not None:
            self.root.after_cancel(self.time_id)
        self.login_register_open = False
        self.root.destroy()