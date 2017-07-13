#!/usr/bin/env python
import sys
from SeatingChart import SeatingChart

USAGE = """\
Default Usage: ./main.py -m 6 -n 8 -o seat.txt -i name.txt
    -h          显示当前帮助并退出
    -m          指定默认行数
    -n          指定默认列数
    -o          指定默认保存的文件
    -i          指定默认输入文件（名单）
    -g          使用图形化界面"""


def get_opts():
    argv = sys.argv[1:]
    res = {
        'USE_GUI': False,
        'DEFAULT_M': 6,
        'DEFAULT_N': 8,
        'DEFAULT_LOAD_FILE': './name.txt',
        'DEFAULT_SAVE_FILE': './seat.txt',
    }
    while argv:
        if argv[0] in ('-h', '--help', '/?'):
            print(USAGE)
            sys.exit(0)
        elif argv[0] == '-g':
            res['USE_GUI'] = True
            argv = argv[1:]
        elif argv[0] == '-m':
            res['DEFAULT_M'] = int(argv[1])
            argv = argv[2:]
        elif argv[0] == '-n':
            res['DEFAULT_N'] = int(argv[1])
            argv = argv[2:]
        elif argv[0] in ('-o', '--output-file'):
            res['DEFAULT_SAVE_FILE'] = argv[1]
            argv = argv[2:]
        elif argv[0] in ('-i', '--input-file'):
            res['DEFAULT_LOAD_FILE'] = argv[1]
            argv = argv[2:]
    return res


opts = get_opts()
if __name__ == '__main__':
    if opts['USE_GUI']:
        import Gui

        Gui.main()
    else:
        seat = SeatingChart(opts['DEFAULT_M'], opts['DEFAULT_N'])
        seat.save(opts['DEFAULT_SAVE_FILE'])
        print("座位表已保存到文件 " + opts['DEFAULT_SAVE_FILE'])
