#!/usr/bin/env python
import sys
import PyQt5.QtWidgets as QWidgets
import PyQt5.QtCore as QCore
from SeatingChart import SeatingChart

WINDOW_TITLE = "随机座位生成器"
DEFAULT_M = 6
DEFAULT_N = 8


class STText(QWidgets.QWidget):
    """用来显示座位表，继承QWidget"""

    def __init__(self, m, n, parent):
        """座位表有m行n列"""
        super().__init__(parent)
        self.seat = SeatingChart(m, n)
        self.name_list = []  # 名单初始时为空， name_list[x] => 学号为x的同学的名字
        ly = QWidgets.QGridLayout(self)
        for i in range(self.seat.m):
            for j in range(self.seat.n):
                ly.addWidget(QWidgets.QLabel(self[i][j]), i, j)
        self.setLayout(ly)

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
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.seat = None

    def make_user_interface(self, m, n):
        self.seat = STText(m, n, self)

        # 创建状态栏
        self.statusBar()

        # 创建动作
        new_action = QWidgets.QAction('新建', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip("新建一张座位表")
        new_action.triggered.connect(self.seat.shuffle)
        save_action = QWidgets.QAction('保存', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip("将座位表保存到文件")
        save_action.triggered.connect(self.save)
        load_action = QWidgets.QAction('载入', self)
        load_action.setShortcut('Ctrl+O')
        load_action.setStatusTip("从文件载入名单")
        load_action.triggered.connect(self.load)
        set_action = QWidgets.QAction('设置', self)
        set_action.setStatusTip("设置字体，建议中文26号，数字48号")
        set_action.triggered.connect(self.set_font)
        quit_action = QWidgets.QAction('退出', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.setStatusTip("退出程序")
        quit_action.triggered.connect(QWidgets.qApp.quit)
        about_action = QWidgets.QAction('关于', self)
        about_action.setStatusTip("显示关于")
        about_action.triggered.connect(self.show_about)

        # 创建工具栏
        file_tools = QWidgets.QToolBar('File')
        file_tools.setMovable(False)
        file_tools.addAction(new_action)
        file_tools.addAction(save_action)
        file_tools.addAction(load_action)
        file_tools.addAction(set_action)
        file_tools.addSeparator()
        file_tools.addAction(quit_action)

        help_tools = QWidgets.QToolBar('Help')
        help_tools.setMovable(False)
        help_tools.addAction(about_action)

        self.addToolBar(QCore.Qt.LeftToolBarArea, file_tools)
        self.addToolBar(QCore.Qt.LeftToolBarArea, help_tools)

        # 创建座位表
        self.setCentralWidget(self.seat)

    def save(self):
        """将座位表保存到文件，显示一个窗口"""
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
        """从文件读取座位表的名单，显示一个窗口"""
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
                error += s + ' '
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
        message.setWindowTitle('关于 ' + WINDOW_TITLE)
        message.setIcon(message.Information)
        show_text = ("""\
        一个简单的随机座位表生成器
        程序全部使用Python编写
        GUI部分使用PyQt5编写
        该程序在GPLv3协议下分发
        详情请参见README
        """)
        message.setText(show_text)
        message.show()


class QueryDialog(QWidgets.QDialog):
    def __init__(self):
        super().__init__()

        layout = QWidgets.QVBoxLayout()
        layout.addWidget(QWidgets.QLabel("请输入座位表的行列数：", self))

        self.box1 = QWidgets.QSpinBox(self)
        self.box2 = QWidgets.QSpinBox(self)

        self.box1.setValue(DEFAULT_M)
        self.box2.setValue(DEFAULT_N)
        self.box1.setSuffix("行")
        self.box2.setSuffix("列")
        layout.addWidget(self.box1)
        layout.addWidget(self.box2)

        button_box = QWidgets.QDialogButtonBox(QWidgets.QDialogButtonBox.Ok |
                                               QWidgets.QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)
        layout.setSizeConstraint(layout.SetMinimumSize)
        self.setFixedHeight(self.minimumHeight())
        self.setWindowTitle("设置")
        self.show()

    def result(self):
        return self.box1.value(), self.box2.value()


if __name__ == '__main__':
    app = QWidgets.QApplication(sys.argv)
    query_dialog = QueryDialog()
    win = Window()
    query_dialog.accepted.connect(lambda: win.make_user_interface(*query_dialog.result()))
    query_dialog.accepted.connect(win.showMaximized)
    query_dialog.rejected.connect(QWidgets.qApp.quit)
    sys.exit(app.exec_())
