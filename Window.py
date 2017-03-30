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
            raise ValueError("名单长度不足")


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
        座位表程序使用Python编写
        GUI使用PyQt5编写
        该程序在GPLv3协议下发布
        """)
        message.setText(show_text)
        message.show()


if __name__ == '__main__':
    app = QWidgets.QApplication(sys.argv)
    win = Window(6, 8)
    sys.exit(app.exec_())
