#!/usr/bin/env python
import sys
from SeatingChart import SeatingChart
import PyQt5.QtWidgets as Qw

SAVE_DEFAULT_FILE = 'seat.txt'
LOAD_DEFAULT_FILE = 'name.txt'


class STText(Qw.QWidget):
    def __init__(self, m, n):
        super().__init__()
        self.seat = SeatingChart(m, n)


class Window(Qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.text = STText(6, 8)
        self.make_user_interface()
        self.setWindowTitle("RSCG")
        self.show()

    def make_user_interface(self):
        # 创建状态栏
        self.statusBar()

        # 创建动作
        new_action = Qw.QAction('新建', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip("新建一张座位表")
        new_action.triggered.connect(self.refresh)
        save_action = Qw.QAction('保存', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip("将座位表保存到文件")
        save_action.triggered.connect(lambda: self.save(SAVE_DEFAULT_FILE))
        load_action = Qw.QAction('载入', self)
        load_action.setShortcut('Ctrl+O')
        load_action.setStatusTip("从文件载入名单")
        load_action.triggered.connect(lambda: self.load(LOAD_DEFAULT_FILE))
        set_action = Qw.QAction('设置', self)
        set_action.setShortcut('Ctrl+S')
        set_action.setStatusTip("设置")
        set_action.triggered.connect(self.setting)
        quit_action = Qw.QAction('退出', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.setStatusTip("退出程序")
        quit_action.triggered.connect(Qw.qApp.quit)
        about_action = Qw.QAction('关于', self)
        about_action.setStatusTip("显示关于")
        about_action.triggered.connect(self.show_about)

        # 创建工具栏
        from PyQt5.QtCore import Qt
        file_tools = Qw.QToolBar('File')
        file_tools.setMovable(False)
        file_tools.addAction(new_action)
        file_tools.addAction(save_action)
        file_tools.addAction(load_action)
        file_tools.addAction(set_action)
        file_tools.addSeparator()

        help_tools = Qw.QToolBar('Help')
        help_tools.setMovable(False)
        file_tools.addAction(quit_action)
        help_tools.addAction(about_action)

        self.addToolBar(Qt.LeftToolBarArea, file_tools)
        self.addToolBar(Qt.LeftToolBarArea, help_tools)

    def refresh(self):
        seat = SeatingChart(6, 8)
        layout = Qw.QGridLayout()
        cent_widget = Qw.QWidget()
        for i in range(seat.m):
            for j in range(seat.n):
                layout.addWidget(Qw.QLabel(seat[i][j].name), i, j)
        cent_widget.setLayout(layout)
        self.setCentralWidget(cent_widget)

    def save(self, file_name):
        pass

    def load(self, file_name):
        pass

    def setting(self):
        pass

    def show_about(self):
        pass


if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())

