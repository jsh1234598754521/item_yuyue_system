# 带有附件的邮件
import smtplib 
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# 设置SMTP服务
mail_host = 'smtp.163.com'
mail_user = 'jsh20140506@163.com'
mail_password = 'NQv48iNpM4KDm5Sh'
mail_port = 587
mail_code = 'NQv48iNpM4KDm5Sh'

# 发邮件用户
sender = 'jsh20140506@163.com'
# 收邮件用户
receivers = ['1621888353@qq.com']         # 如果要群发 直接逗号即可(receivers = ['jsh20140506@163.com'，'群发目标'])

'''
邮件的纯文本部分
'''
# 邮件内容
msg = '''尊敬的陈女士：
            您的银行卡已被冻结！请及时去营业厅解冻！网址：https://www.baidu.com/'''      # 内容自定义
# 主题设置
title = '厦门银行'            # 内容可自定义
# 信息的转化        
message = MIMEText(msg,'plain','utf8')

'''
邮件的附件部分
'''
image_path = 'SMTP邮箱邮件发送学习/附件列表/icons8-视窗11-48.png'
image_name = 'windows.png'
image_part = MIMEImage(open(image_path,'rb').read(),image_path.split('.')[-1])
# Content-Disposition:保证图片可以显示
# attachment:保证已发送的附件可以阅览和下载
image_part.add_header('Content-Disposition','attachment',filename=image_name)
# 第二个图片
image_path_1 = 'SMTP邮箱邮件发送学习/附件列表/zip.png'
image_name_1 = 'zip.png'
image_part_1 = MIMEImage(open(image_path_1,'rb').read(),image_path_1.split('.')[-1])
# Content-Disposition:保证图片可以显示
# attachment:保证已发送的附件可以阅览和下载
image_part_1.add_header('Content-Disposition','attachment',filename=image_name_1)

# python文档发送
python_path = 'main_dos.py'
python_name = '公共物品预约.py'
python_part = MIMEApplication(open(python_path,'rb').read(),python_path.split('.')[-1])
# Content-Disposition:保证图片可以显示
# attachment:保证已发送的附件可以阅览和下载
python_part.add_header('Content-Disposition','attachment',filename=python_name)


# 邮件内容与附件进行拼接
m = MIMEMultipart()
m.attach(message)
m.attach(image_part)
m.attach(image_part_1)
m.attach(python_part)

# 发送邮件
# 邮件发送者
m['From'] = '{}'.format(sender)
# 邮件接收者
m['To'] = ','.join(receivers)
# 设置主题
m['Subject'] = title
# 登录用户
server = smtplib.SMTP_SSL(mail_host,mail_port)
server.login(mail_user,mail_code)
# 发送邮件
server.sendmail(sender,'jsh20140506@163.com',m.as_string())

# 退出服务
server.quit()
