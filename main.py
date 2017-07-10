#!/usr/bin/env python
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
    import sys
    argv = sys.argv
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
        elif argv[0] == '-m':
            argv = argv[1:]
            res['DEFAULT_M'] = int(argv[0])
        elif argv[0] == '-n':
            argv = argv[1:]
            res['DEFAULT_N'] = int(argv[0])
        elif argv[0] in ('-o', '--output-file'):
            argv = argv[1:]
            res['DEFAULT_SAVE_FILE'] = argv[0]
        elif argv[0] in ('-i', '--input-file'):
            argv = argv[1:]
            res['DEFAULT_LOAD_FILE'] = argv[0]
        argv = argv[1:]
    return res


# TODO:单元测试

opts = get_opts()
if __name__ == '__main__':
    if opts['USE_GUI']:
        import Gui
    else:
        seat = SeatingChart(opts['DEFAULT_M'], opts['DEFAULT_N'])
        seat.save(opts['DEFAULT_SAVE_FILE'])
        print("座位表已保存到文件 " + opts['DEFAULT_SAVE_FILE'])
