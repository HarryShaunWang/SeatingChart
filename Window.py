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
        layout = Qw.QGridLayout(self)
        for i in range(self.seat.m):
            for j in range(self.seat.n):
                layout.addWidget(Qw.QLabel(self[i][j]), i, j)
        self.setLayout(layout)

    def __getitem__(self, i):
        return [self.name_list[x] if self.name_list else str(x) for x in self.seat[i]]

    def __repr__(self):
        return str(self.seat)

    def __str__(self):
        s = ''
        for i in range(self.seat.m):
            for j in range(self.seat.n):
                s += self[i][j]
                if i % 2 == 1 and i + 1 != self.seat.n:
                    s += '||'
        return s

    def shuffle(self):
        self.seat.shuffle()
        for i in range(self.seat.m):
            for j in range(self.seat.n):
                self.layout().itemAtPosition(i, j).widget().setText(self[i][j])

    def set_name(self, names: list):
        names.insert(0, '空桌子')
        if len(names) >= len(self.seat):
            self.name_list = names
            for i in range(self.seat.m):
                for j in range(self.seat.n):
                    self.layout().itemAtPosition(i, j).widget().setText(self[i][j])
        else:
            raise ValueError("名单长度不足")


class Window(Qw.QMainWindow):
    def __init__(self, m, n):
        super().__init__()
        self.name_list = []
        self.seat = STText(m, n, self)
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
        new_action.triggered.connect(self.seat.shuffle)
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

        from PyQt5.QtCore import Qt
        self.addToolBar(Qt.LeftToolBarArea, file_tools)
        self.addToolBar(Qt.LeftToolBarArea, help_tools)

        # 创建座位表
        self.setCentralWidget(self.seat)

    def save(self):
        file_dia = Qw.QFileDialog(self)
        file = file_dia.getSaveFileName(self)
        if file[0] and open(file[0], 'w').writable():
            open(file[0], 'w').write(self.centralWidget().__str__())

    def load(self):
        file_dia = Qw.QFileDialog(self)
        file = file_dia.getOpenFileName(self)
        if file[0] and open(file[0], 'r').readable():
            self.centralWidget().set_name(open(file[0], 'r').read().split())

    def setting(self):
        font_dia = Qw.QFontDialog(self)
        font, ok = font_dia.getFont(self)
        if ok:
            self.centralWidget().setFont(font)

    def show_about(self):
        pass


if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    win = Window(6, 8)
    sys.exit(app.exec_())
