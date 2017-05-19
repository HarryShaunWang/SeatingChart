#!/usr/bin/env python
import sys
from SeatingChart import SeatingChart

DEFAULT_M = 6
DEFAULT_N = 8
DEFAULT_LOAD_FILE = './name.txt'
DEFAULT_SAVE_FILE = './seat.txt'

if __name__ == '__main__':
    for index, opt in enumerate(sys.argv):
        if opt in ('-h', '--help'):
            print("""\
            Default Usage:
                ./main.py -m 6 -n 8 -o seat.txt -i name.txt --no-gui
            -h          显示当前帮助并退出
            -m          指定默认行数
            -n          指定默认列数
            -o          指定默认保存的文件
            -i          指定默认输入文件（名单）
            --no-gui    不显示图形化界面""")
            sys.exit()
        elif opt == '-m':
            DEFAULT_M = sys.argv[index + 1]
        elif opt == '-n':
            DEFAULT_N = sys.argv[index + 1]
        elif opt in ('-o', '--output-file'):
            DEFAULT_SAVE_FILE = sys.argv[index + 1]
        elif opt in ('-i', '--input-file'):
            DEFAULT_LOAD_FILE = sys.argv[index + 1]
    else:
        if '--no-gui' not in sys.argv:
            import gui

            app = gui.QApplication(sys.argv)
            init_dialog = gui.InitDialog()
            win = gui.Window()
            init_dialog.accepted.connect(lambda: win.init_ui(init_dialog.box1.value(), init_dialog.box2.value()))
            init_dialog.accepted.connect(win.showMaximized)
            init_dialog.rejected.connect(gui.qApp.quit)
            sys.exit(app.exec_())
        else:
            seat = SeatingChart(DEFAULT_M, DEFAULT_N)
            seat.save(DEFAULT_SAVE_FILE)
            print("座位表已保存到文件 " + DEFAULT_SAVE_FILE)
