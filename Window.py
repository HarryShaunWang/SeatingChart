#!/usr/bin/env python
import sys
import PyQt5.QtWidgets as Qw
from SeatingChart import SeatingChart


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
        try:
            names.insert(0, '空桌子')
            if len(names) >= len(self.seat):
                self.name_list = names
                for i in range(self.seat.m):
                    for j in range(self.seat.n):
                        self.layout().itemAtPosition(i, j).widget().setText(self[i][j])
            else:
                raise ValueError("名单长度不足")
        except ValueError as err:
            for s in err.args:
                print(s)


class Window(Qw.QMainWindow):
    def __init__(self, m, n):
        super().__init__()
        self.name_list = []
        self.seat = STText(m, n, self)
        self.make_user_interface()
        self.setWindowTitle("RSCG")
        self.show()

    class NormalAction(Qw.QAction):
        def __init__(self, text, short_cut, status_tip, trig, parent):
            Qw.QAction.__init__(self, text, parent)
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
        set_action = self.NormalAction('设置', 'Ctrl+S', "设置字体", self.set_font, self)
        quit_action = self.NormalAction('退出', 'Ctrl+Q', "退出程序", Qw.qApp.quit, self)
        about_action = self.NormalAction('关于', None, "显示关于", self.show_about, self)

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
        file_dia.setWindowTitle('读取名单')
        file = file_dia.getOpenFileName(self)
        if file[0] and open(file[0], 'r').readable():
            self.centralWidget().set_name(open(file[0], 'r').read().split())

    def set_font(self):
        font_dia = Qw.QFontDialog(self)
        font, ok = font_dia.getFont(self)
        if ok:
            self.centralWidget().setFont(font)

    def show_about(self):
        message = Qw.QMessageBox(self)
        message.setWindowTitle('关于')
        message.setIcon()
        show_text = ("""
        一个简单的随机座位表生成器
        座位表程序使用Python编写
        GUI使用PyQt5编写
        """)
        message.setText(show_text)
        message.show()


if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    win = Window(6, 8)
    sys.exit(app.exec_())
