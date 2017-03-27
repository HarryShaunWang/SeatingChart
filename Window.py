#!/usr/bin/env python
import sys
from SeatingChart import SeatingChart
import PyQt5.QtWidgets as Qw

SAVE_DEFAULT_FILE = 'seat.txt'
LOAD_DEFAULT_FILE = 'name.txt'


class STText(Qw.QWidget):
    def __init__(self, m, n, parent):
        super().__init__(parent)
        self.name_list = []
        self.seat = SeatingChart(m, n)
        self.mk_layout()

    def __getitem__(self, i):
        return [self.name_list[x] if self.name_list else str(x) for x in self.seat[i]]

    def __str__(self):
        return str(self.seat)

    def mk_layout(self):
        layout = Qw.QGridLayout(self)
        for i in range(self.seat.m):
            for j in range(self.seat.n):
                label = Qw.QLabel(self)
                label.setText(self[i][j])
                layout.addWidget(label, i, j)
        self.setLayout(layout)

    def shuffle(self):
        self.seat.shuffle()
        self.mk_layout()

    def load_name(self, names):
        if len(names) >= len(self.seat):
            self.name_list = names
        else:
            raise ValueError("名单长度不足")


class Window(Qw.QMainWindow):
    def __init__(self, m, n):
        super().__init__()
        self.name_list = []
        self.cent_setting = {'m': m, 'n': n, 'font': self.font()}
        self.make_user_interface(m, n)
        self.setWindowTitle("RSCG")
        self.show()

    def make_user_interface(self, m, n):
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
        save_action.triggered.connect(self.save)
        load_action = Qw.QAction('载入', self)
        load_action.setShortcut('Ctrl+O')
        load_action.setStatusTip("从文件载入名单")
        load_action.triggered.connect(self.load)
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

        self.refresh()

    def refresh(self):
        seat = STText(self.cent_setting['m'], self.cent_setting['n'], self)
        seat.setFont(self.cent_setting['font'])
        self.setCentralWidget(seat)
        print(seat)
        self.show()

    def save(self):
        file_dia = Qw.QFileDialog(self)
        file_dia.setAcceptMode(file_dia.AcceptSave)
        file = file_dia.getSaveFileName(self)
        if file[0]:
            with open(file[0], 'w'):
                open(file[0], 'w').write(self.centralWidget().__str__())

    def load(self):
        file_dia = Qw.QFileDialog(self)
        file_dia.setAcceptMode(file_dia.AcceptOpen)
        file = file_dia.getOpenFileName(self)
        if file[0]:
            with open(file[0], 'r'):
                self.centralWidget().set_name(open(file[0], 'r').read().split())

    def setting(self):
        font_dia = Qw.QFontDialog(self)
        font, ok = font_dia.getFont(self)
        if ok:
            self.cent_setting['font'] = font
            self.centralWidget().set(self.cent_setting)

    def show_about(self):
        pass


if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    win = Window(6, 8)
    sys.exit(app.exec_())
