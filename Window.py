#!/usr/bin/env python
from tkinter import *
from SeatingChart import SeatingChart

LABEL_FONT = ('times', 20, 'normal')
TEXT_FONT = ('courier', 28, 'normal')
BUTTON_FONT = ('times', 16, 'bold')
SAVE_DEFAULT_FILE = 'seat.txt'
LOAD_DEFAULT_FILE = 'name.txt'


class BeautifulButton(Button):
    """一种稍加美化的按钮"""

    def __init__(self, master=None, **config):
        Button.__init__(self, master=master, **config)
        self.config(heigh=1, width=12)
        self.config(font=BUTTON_FONT)


class STText(SeatingChart, Text):
    """用部件保存并且显示一个座位表 """

    def __init__(self, m, n, master=None, **config):
        SeatingChart.__init__(self, m, n)
        Text.__init__(self, master, **config)
        self._a = []
        self.get_name(use='default')
        self.config(font=TEXT_FONT)
        self.config(heigh=12, width=82)
        self.refresh()

    def __str__(self):
        s = ""
        for i in range(self.m):
            for j in range(self.n):
                name = self._a[self[i][j]] if self._a else str(self[i][j])
                s += (8 - len(name) * 2) * ' ' + name
                if j % 2 == 1 and j + 1 != self.n:
                    s += '||'
            s += '\n'
        return s

    def __len__(self):
        return SeatingChart.__len__(self)

    def refresh(self):
        """随机打乱座位顺序并显示在屏幕上"""
        self.shuffle()
        self.config(state=NORMAL)
        self.delete('0.0', END)
        self.insert('0.0', self.__str__())
        self.config(state=DISABLED)

    def get_name(self, file_name='name.txt', **config):
        """从文件file_name中读取一份名单
        若名单长度不足总人数则显示一个错误，否则读取名单中前N的名字
        名单中名字出现的顺序应该对应学号的顺序"""
        import os
        from tkinter.messagebox import showerror
        if os.path.exists(file_name):
            name = open(file_name, 'r').read().split()
            name.insert(0, "空桌子")
            if len(name) >= len(self):
                self._a = name
                self.refresh()
            else:
                showerror(title='错误', message="文件 %s 中人数不足！" % file_name)
        else:
            if 'use' not in config:
                showerror(title='错误', message="%s 不存在！" % file_name)

    def save_to_file(self, file_name='seat.txt'):
        """把座位表以可读的形式保存到file_name中"""
        from tkinter.messagebox import showinfo, askyesno
        import os
        if not os.path.exists(file_name) or askyesno(title='确定', message="%s 已经存在，是否覆盖？" % file_name):
            f_out = open(file_name, 'w')
            f_out.write(str(self))
            showinfo(title='保存成功', message='座位已经保存到 %s 中！' % file_name)
            f_out.close()


class _FileWindow(Toplevel):
    """显示文件交互的窗口，包括一行消息，一个输入框，一个行为按钮，一个取消按钮"""

    def __init__(self, master):
        Toplevel.__init__(self, master=master)
        Label(self, text="输入文件名", font=LABEL_FONT).pack(expand=YES, fill=X)  # 文字说明
        self.file_name = Entry(self, font=LABEL_FONT)  # 输入框
        self.file_name.pack(expand=YES, fill=BOTH)
        self.file_name.focus()
        self.act_but = BeautifulButton(self)  # 行为按钮
        self.act_but.pack(side=LEFT, fill=X)
        BeautifulButton(self, text='取消', command=self.destroy).pack(side=RIGHT, fill=X)  # 取消按钮
        self.bind('<Return>', lambda event: self.active(self.file_name.get()))
        self.grab_set()

    def active(self, file_name): pass


class SaveWindow(_FileWindow):
    """保存窗口，把名字保存到文件"""

    def __init__(self, master):
        _FileWindow.__init__(self, master)
        self.title('保存到文件')
        self.act_but.config(text='保存', command=lambda: self.active(self.file_name.get()))
        self.file_name.insert(0, SAVE_DEFAULT_FILE)
        self.file_name.select_range(0, END)

    def active(self, file_name):
        chart.save_to_file(file_name)
        self.destroy()


class LoadWindow(_FileWindow):
    """载入窗口，加载姓名"""

    def __init__(self, master):
        _FileWindow.__init__(self, master)
        self.title('从文件读取')
        self.act_but.config(text='读取', command=lambda: self.active(self.file_name.get()))
        self.file_name.insert(0, LOAD_DEFAULT_FILE)
        self.file_name.select_range(0, END)

    def active(self, file_name):
        chart.get_name(file_name)
        self.destroy()


def show_about():
    """显示关于信息"""
    about = Toplevel()
    about.title('关于')
    show_txt = ("""
    一个简单的随机座位生成器。
    由Python3编写
    使用Tk图形库
    """)
    Label(about, text=show_txt, heigh=24).pack(fill=X)
    but = BeautifulButton(about, text='确定', command=about.destroy)
    but.pack(fill=X, side=BOTTOM)
    but.focus()
    about.grab_set()


if __name__ == '__main__':
    root = Tk()
    root.title('座位生成器')
    chart = STText(m=6, n=8, master=root)

    # 顶部菜单
    top_menu = Menu(root)
    # File菜单
    file_menu = Menu(top_menu)
    file_menu.config(tearoff=False)
    file_menu.add_command(label='新建...', command=chart.refresh, underline=0)
    file_menu.add_command(label='另存为...', command=(lambda: SaveWindow(root)), underline=0)
    file_menu.add_command(label='读取...', command=(lambda: LoadWindow(root)), underline=0)
    file_menu.add_separator()
    file_menu.add_command(label='退出...', command=root.destroy, underline=0)
    # Help菜单
    help_menu = Menu(top_menu)
    help_menu.config(tearoff=False)
    help_menu.add_command(label='关于...', command=show_about, underline=0)
    # 添加菜单到程序顶部
    root.config(menu=top_menu)
    top_menu.add_cascade(label='文件', menu=file_menu, underline=0)
    top_menu.add_cascade(label='帮助', menu=help_menu, underline=0)

    # 文字部分
    label_frame = Frame(root)
    tmp_frame1, tmp_frame2 = Frame(label_frame), Frame(label_frame)
    Label(tmp_frame1, text="点击新建生成一个新的座位表", font=LABEL_FONT).pack()
    Label(tmp_frame2, text="点击保存将座位表保存到文件", font=LABEL_FONT).pack()
    tmp_frame1.pack(side=LEFT, expand=YES, fill=X)
    tmp_frame2.pack(side=RIGHT, expand=YES, fill=X)
    label_frame.pack(expand=YES, fill=BOTH)
    chart.pack(expand=YES, fill=BOTH)

    # 屏幕下方部件
    bot = Frame(root)
    bot.pack(side=BOTTOM, fill=X)
    b_new = BeautifulButton(bot, text='新建', command=chart.refresh)


    def locked():
        b_new.forget()
        b_lock.forget()
        tmp_frame1.forget()
        file_menu.delete(0, 0)
        file_menu.delete(1, 1)


    b_lock = BeautifulButton(bot, text='锁定', command=locked)
    b_save_as = BeautifulButton(bot, text='保存', command=(lambda: chart.save_to_file(e_ent.get())))
    e_ent = Entry(bot, font=LABEL_FONT)
    e_ent.insert(0, SAVE_DEFAULT_FILE)
    b_quit = BeautifulButton(bot, text='退出', command=root.destroy)
    b_new.pack(side=LEFT)
    b_lock.pack(side=LEFT)
    b_save_as.pack(side=LEFT)
    e_ent.pack(expand=YES, fill=BOTH, side=LEFT)
    b_quit.pack(side=RIGHT)

    root.bind('<Return>', (lambda event: chart.save_to_file(e_ent.get())))
    root.wait_window()
    root.mainloop()
