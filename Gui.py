import sys
from main import opts
from SeatingChart import SeatingChart
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

WINDOW_TITLE = '随机座位生成器'
ABOUT = """\
一个简单的随机座位表生成器
使用Python编写
GUI部分使用PyQt5编写
该程序在GPLv3协议下分发
详情请参见README"""


# TODO:需要一个GUI规则编辑器
class RuleEditor:
    pass


class _SeatingWidget(QTableWidget):
    # TODO:座位表拖放编辑功能
    # TODO:添加走廊显示
    def __init__(self, m, n, parent):
        super().__init__(m, n, parent)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.seat = SeatingChart(m, n)
        self.setVerticalHeaderLabels(['第{}行'.format(i + 1) for i in range(self.seat.m)])
        self.setHorizontalHeaderLabels(['第{}列'.format(i + 1) for i in range(self.seat.n)])
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(self.seat.m):
            for j in range(self.seat.n):
                table_widget_item = QTableWidgetItem()
                table_widget_item.setFlags(Qt.ItemIsEnabled)
                self.setItem(i, j, table_widget_item)
        self.gen_text()

    def shuffle(self):
        self.seat.shuffle()
        self.gen_text()

    def load(self, file_name):
        self.seat.load(file_name)
        self.gen_text()

    def save(self, file_name):
        self.seat.save(file_name)

    def gen_text(self):
        for i in range(self.seat.m):
            for j in range(self.seat.n):
                self.item(i, j).setText(self.seat.get_name(i, j))

    def set_font(self, font: QFont):
        for i in range(self.seat.m):
            for j in range(self.seat.n):
                self.item(i, j).setFont(font)


class Window(QMainWindow):
    # TODO:座位表之间的回滚
    def __init__(self):
        super().__init__()
        self.seat_stack = [range(10, 1, -1)]
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowFilePath(opts['DEFAULT_LOAD_FILE'])
        self.seat_table = None

    def init_ui(self, m, n):
        # 创建座位表
        self.seat_table = _SeatingWidget(m, n, self)

        # 创建状态栏
        self.statusBar()

        # 创建动作
        new_action = QAction(QIcon.fromTheme('document-new'), '新建', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip("新建一张座位表")
        new_action.triggered.connect(self.seat_table.shuffle)
        save_action = QAction(QIcon.fromTheme('document-save'), '保存', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip("将座位表保存到文件")
        save_action.triggered.connect(self.save)
        load_action = QAction(QIcon.fromTheme('document-open'), '载入', self)
        load_action.setShortcut('Ctrl+O')
        load_action.setStatusTip("从文件载入名单")
        load_action.triggered.connect(self.load)
        set_action = QAction(QIcon.fromTheme('preferences-desktop-font'), '设置字体', self)
        set_action.setStatusTip("设置字体，建议中文26号，数字48号")
        set_action.triggered.connect(self.set_font)
        quit_action = QAction(QIcon.fromTheme('application-exit'), '退出', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.setStatusTip("退出程序")
        quit_action.triggered.connect(qApp.quit)
        about_action = QAction(QIcon.fromTheme('help-about'), '关于', self)
        about_action.setStatusTip("显示关于")
        about_action.triggered.connect(lambda: QMessageBox().about(self, '关于 ' + WINDOW_TITLE, ABOUT))
        about_qt_action = QAction('关于 Qt', self)
        about_qt_action.setStatusTip("显示关于 Qt")
        about_qt_action.triggered.connect(lambda: QMessageBox().aboutQt(self))

        # 创建菜单栏
        menus = self.menuBar()

        file_menu = menus.addMenu('文件')
        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)
        file_menu.addAction(set_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

        help_menu = menus.addMenu('帮助')
        help_menu.addAction(about_action)
        help_menu.addAction(about_qt_action)

        self.setCentralWidget(self.seat_table)

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
        # TODO:滚动调节字体
        font_dia = QFontDialog(self)
        font, ok = font_dia.getFont(self)
        if ok:
            self.seat_table.set_font(font)


class InitDialog(QDialog):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("请输入座位表的行列数：", self))

        self.box1 = QSpinBox(self)
        self.box2 = QSpinBox(self)

        self.box1.setValue(opts['DEFAULT_M'])
        self.box2.setValue(opts['DEFAULT_N'])
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


app = QApplication(sys.argv)
init_dialog = InitDialog()
win = Window()
init_dialog.accepted.connect(lambda: win.init_ui(init_dialog.box1.value(), init_dialog.box2.value()))
init_dialog.accepted.connect(win.showMaximized)
init_dialog.rejected.connect(qApp.quit)
sys.exit(app.exec_())
