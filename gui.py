from main import (DEFAULT_M, DEFAULT_N, DEFAULT_LOAD_FILE)
from SeatingChart import SeatingChart
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, qApp,
                             QMainWindow, QWidget, QAction,
                             QLabel, QToolBar, QSpinBox, QDialogButtonBox, QMessageBox,
                             QDialog, QFileDialog, QErrorMessage, QFontDialog,
                             QGridLayout, QVBoxLayout)


class _SeatingWidget(QWidget):
    def __init__(self, m, n, parent):
        super().__init__(parent)
        self.seat = SeatingChart(m, n)
        ly = QGridLayout(self)
        for i in range(self.seat.m):
            for j in range(self.seat.n):
                ly.addWidget(QLabel(self[i][j]), i, j)
        self.setLayout(ly)

    def __getitem__(self, i):
        return self.seat[i]

    def __str__(self):
        return str(self.seat)

    def shuffle(self):
        self.seat.shuffle()
        self.refresh_text()

    def load(self, file_name):
        self.seat.load(file_name)
        self.refresh_text()

    def save(self, file_name):
        self.seat.save(file_name)

    def refresh_text(self):
        for i in range(self.seat.m):
            for j in range(self.seat.n):
                self.layout().itemAtPosition(i, j).widget().setText(self[i][j])


class Window(QMainWindow):
    WINDOW_TITLE = "随机座位生成器"
    ABOUT = """\
一个简单的随机座位表生成器
程序使用Python编写
GUI部分使用PyQt5编写
该程序在GPLv3协议下分发
详情请参见README"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFilePath(DEFAULT_LOAD_FILE)
        self.seat = None

    def init_ui(self, m, n):
        # 创建座位表
        self.seat = _SeatingWidget(m, n, self)
        self.setCentralWidget(self.seat)

        # 创建状态栏
        self.statusBar()

        # 创建动作
        new_action = QAction('新建', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip("新建一张座位表")
        new_action.triggered.connect(self.seat.shuffle)
        save_action = QAction('保存', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip("将座位表保存到文件")
        save_action.triggered.connect(self.save)
        load_action = QAction('载入', self)
        load_action.setShortcut('Ctrl+O')
        load_action.setStatusTip("从文件载入名单")
        load_action.triggered.connect(self.load)
        set_action = QAction('设置', self)
        set_action.setStatusTip("设置字体，建议中文26号，数字48号")
        set_action.triggered.connect(self.set_font)
        quit_action = QAction('退出', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.setStatusTip("退出程序")
        quit_action.triggered.connect(qApp.quit)
        about_action = QAction('关于', self)
        about_action.setStatusTip("显示关于")
        about_action.triggered.connect(lambda: QMessageBox().about(self, '关于 ' + self.WINDOW_TITLE, self.ABOUT))

        # 创建工具栏
        file_tools = QToolBar('File')
        file_tools.addAction(new_action)
        file_tools.addAction(save_action)
        file_tools.addAction(load_action)
        file_tools.addAction(set_action)
        file_tools.addSeparator()
        file_tools.addAction(quit_action)

        help_tools = QToolBar('Help')
        help_tools.addAction(about_action)

        self.addToolBar(file_tools)
        self.addToolBar(help_tools)

    def save(self):
        """将座位表保存到文件，显示一个窗口"""
        file_dia = QFileDialog(self)
        file_dia.setAcceptMode(file_dia.AcceptSave)
        file = file_dia.getSaveFileName(self, "保存文件", self.windowFilePath(), "文本文件(*.txt);;所有文件(*.*)")
        try:
            if file[0]:
                self.centralWidget().save(file[0])
                self.setWindowFilePath(file[0])
                show_message = QMessageBox(self)
                show_message.setWindowTitle('完成')
                show_message.setIcon(show_message.Information)
                show_message.setText("文件已成功保存到{file_name}。".format(file_name=file[0]))
                show_message.show()
        except IOError as err:
            err_message = QErrorMessage(self)
            err_message.setWindowTitle(err.filename)
            err_message.showMessage("{err}\n这不是一个有效的文件！".format(err=err.args))
        except PermissionError as err:
            err_message = QErrorMessage(self)
            err_message.setWindowTitle(err.filename)
            err_message.showMessage("{err}\n这不是一个有效的文件！".format(err=err.strerror))

    def load(self):
        """从文件读取座位表的名单，显示一个窗口"""
        file_dia = QFileDialog(self)
        file_dia.setAcceptMode(file_dia.AcceptOpen)
        file = file_dia.getOpenFileName(self, "读取名单", self.windowFilePath(), "文本文件(*.txt);;所有文件(*.*)")
        try:
            if file[0]:
                self.centralWidget().load(file[0])
                self.setWindowFilePath(file[0])
        except ValueError as err:
            err_message = QErrorMessage(self)
            error = ""
            for s in err.args:
                error += s + ' '
            err_message.showMessage("{err}！".format(err=error))
        except PermissionError as err:
            err_message = QErrorMessage(self)
            error = ""
            for s in err.args:
                error += s
            err_message.showMessage("{err}！".format(err=error))

    def set_font(self):
        """设置显示座位表的字体"""
        font_dia = QFontDialog(self)
        font, ok = font_dia.getFont(self.centralWidget().font(), self)
        if ok:
            self.centralWidget().setFont(font)


class InitDialog(QDialog):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("请输入座位表的行列数：", self))

        self.box1 = QSpinBox(self)
        self.box2 = QSpinBox(self)

        self.box1.setValue(DEFAULT_M)
        self.box2.setValue(DEFAULT_N)
        self.box1.setSuffix("行")
        self.box2.setSuffix("列")
        layout.addWidget(self.box1)
        layout.addWidget(self.box2)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)
        layout.setSizeConstraint(layout.SetMinimumSize)
        self.setFixedHeight(self.minimumHeight())
        self.setWindowTitle("设置")
        self.show()


