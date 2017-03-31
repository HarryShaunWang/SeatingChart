#!/usr/bin/env python
import sys
import PyQt5.QtWidgets as QWidgets
import PyQt5.QtCore as QCore
from SeatingChart import SeatingChart


class STText(QWidgets.QWidget):
    """用来显示座位表，继承QWidget"""

    def __init__(self, m, n, parent):
        """座位表有m行n列"""
        super().__init__(parent)
        self.seat = SeatingChart(m, n)
        self.name_list = []  # 名单初始时为空， name_list[x] => 学号为x的同学的名字
        layout = QWidgets.QGridLayout(self)
        for i in range(self.seat.m):
            for j in range(self.seat.n):
                layout.addWidget(QWidgets.QLabel(self[i][j]), i, j)
        self.setLayout(layout)

    def __getitem__(self, i):
        """返回第i行同学的名单"""
        return [(self.name_list[x] if self.name_list else str(x)) for x in self.seat[i]]

    def __str__(self):
        """返回可视化的座位表"""
        s = ''
        for i in range(self.seat.m):
            for j in range(self.seat.n):
                s += self[i][j].rjust(4)
                if j % 2 == 1 and j + 1 != self.seat.n:
                    s += '||'
            s += '\n'
        return s

    def shuffle(self):
        """随机打乱座位"""
        self.seat.shuffle()
        for i in range(self.seat.m):
            for j in range(self.seat.n):
                self.layout().itemAtPosition(i, j).widget().setText(self[i][j])

    def set_name(self, names):
        """"设置班级名单"""
        names.insert(0, '空桌子')
        if len(names) >= len(self.seat):
            self.name_list = names[0: len(self.seat)]
            for i in range(self.seat.m):
                for j in range(self.seat.n):
                    self.layout().itemAtPosition(i, j).widget().setText(self[i][j])
        else:
            raise ValueError("名单长度不足{num}".format(num=len(self.seat)))


class Window(QWidgets.QMainWindow):
    def __init__(self, m, n):
        """窗口中座位表有m行n列"""
        super().__init__()
        self.seat = STText(m, n, self)
        self.setWindowTitle('随机座位生成器')
        self.setWindowState(QCore.Qt.WindowMaximized)
        self.make_user_interface()
        self.show()

    class NormalAction(QWidgets.QAction):
        """打包过的QAction类"""

        def __init__(self, text, short_cut, status_tip, trig, parent):
            QWidgets.QAction.__init__(self, text, parent)
            if short_cut:
                self.setShortcut(short_cut)
            if status_tip:
                self.setStatusTip(status_tip)
            if trig:
                self.triggered.connect(trig)

    def make_user_interface(self):
        # 创建状态栏
        self.statusBar()

        # 创建动作
        new_action = self.NormalAction('新建', 'Ctrl+N', "新建一张座位表", self.seat.shuffle, self)
        save_action = self.NormalAction('保存', 'Ctrl+S', "将座位表保存到文件", self.save, self)
        load_action = self.NormalAction('载入', 'Ctrl+O', "从文件载入名单", self.load, self)
        set_action = self.NormalAction('设置', 'Ctrl+S', "设置字体，建议中文26号，数字48号", self.set_font, self)
        quit_action = self.NormalAction('退出', 'Ctrl+Q', "退出程序", QWidgets.qApp.quit, self)
        about_action = self.NormalAction('关于', None, "显示关于", self.show_about, self)

        # 创建工具栏
        file_tools = QWidgets.QToolBar('File')
        file_tools.setMovable(False)
        file_tools.addAction(new_action)
        file_tools.addAction(save_action)
        file_tools.addAction(load_action)
        file_tools.addAction(set_action)
        file_tools.addSeparator()

        help_tools = QWidgets.QToolBar('Help')
        help_tools.setMovable(False)
        file_tools.addAction(quit_action)
        help_tools.addAction(about_action)

        self.addToolBar(QCore.Qt.LeftToolBarArea, file_tools)
        self.addToolBar(QCore.Qt.LeftToolBarArea, help_tools)

        # 创建座位表
        self.setCentralWidget(self.seat)

    def save(self):
        """显示一个保存文件的窗口"""
        file_dia = QWidgets.QFileDialog(self)
        file_dia.setAcceptMode(file_dia.AcceptSave)
        file = file_dia.getSaveFileName(self, "保存文件", self.windowFilePath(), "文本文件(*.txt);;所有文件(*.*)")
        try:
            if file[0]:
                open(file[0], 'w').write(self.centralWidget().__str__())
                self.setWindowFilePath(file[0])
                show_message = QWidgets.QMessageBox(self)
                show_message.setWindowTitle('完成')
                show_message.setIcon(show_message.Information)
                show_message.setText("文件已成功保存到{file_name}。".format(file_name=file[0]))
                show_message.show()
        except IOError as err:
            err_message = QWidgets.QErrorMessage(self)
            err_message.setWindowTitle(err.filename)
            err_message.showMessage("{err}\n这不是一个有效的文件！".format(err=err.args))
        except PermissionError as err:
            err_message = QWidgets.QErrorMessage(self)
            err_message.setWindowTitle(err.filename)
            err_message.showMessage("{err}\n这不是一个有效的文件！".format(err=err.strerror))

    def load(self):
        """显示一个载入文件的系统"""
        file_dia = QWidgets.QFileDialog(self)
        file_dia.setAcceptMode(file_dia.AcceptOpen)
        file = file_dia.getOpenFileName(self, "读取名单", self.windowFilePath(), "文本文件(*.txt);;所有文件(*.*)")
        try:
            if file[0]:
                names = open(file[0], 'r').read().split()
                self.centralWidget().set_name(names)
                self.setWindowFilePath(file[0])
        except ValueError as err:
            err_message = QWidgets.QErrorMessage(self)
            error = ""
            for s in err.args:
                error += s
            err_message.showMessage("{err}！".format(err=error))
        except PermissionError as err:
            err_message = QWidgets.QErrorMessage(self)
            error = ""
            for s in err.args:
                error += s
            err_message.showMessage("{err}！".format(err=error))

    def set_font(self):
        """设置显示座位表的字体"""
        font_dia = QWidgets.QFontDialog(self)
        font, ok = font_dia.getFont(self.centralWidget().font(), self)
        if ok:
            self.centralWidget().setFont(font)

    def show_about(self):
        """显示关于窗口"""
        message = QWidgets.QMessageBox(self)
        message.setWindowTitle('关于')
        message.setIcon(message.Information)
        show_text = ("""
        一个简单的随机座位表生成器
        程序全部使用Python编写
        GUI部分使用PyQt5编写
        该程序在GPLv3协议下分发
        详情请参见README
        """)
        message.setText(show_text)
        message.show()


if __name__ == '__main__':
<<<<<<< HEAD
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

=======
    app = QWidgets.QApplication(sys.argv)
    win = Window(6, 8)
    sys.exit(app.exec_())
>>>>>>> PyQt
