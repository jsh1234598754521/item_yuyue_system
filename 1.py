from ttkbootstrap import Window, Checkbutton, Button, Frame, Toplevel, Label
from tkinter import IntVar

# 弹窗函数
def open_policy():
    policy_win = Toplevel(root)
    policy_win.transient(root)
    policy_win.title("政策说明")
    policy_win.geometry("550x350")
    frm = Frame(policy_win, padding=20)
    frm.pack(fill="both", expand=True)
    Label(frm, text="服务政策条款", font=("",14,"bold")).pack(pady=(0,12))
    content = "这里填写你的政策文本内容\n多条内容自动换行展示"
    Label(frm, text=content, wraplength=500, justify="left").pack()

# 主窗口
root = Window()
root.title("演示")
var = IntVar()

# 横向容器
container = Frame(root, padding=15)
container.pack()

# 复选框（无文字）
Checkbutton(container, variable=var).pack(side="left")

# link样式按钮模拟超链接
link_btn = Button(
    container,
    text="查看完整政策",
    bootstyle="link",
    cursor="hand2",
    command=open_policy
)
link_btn.pack(side="left", padx=6)

root.mainloop()