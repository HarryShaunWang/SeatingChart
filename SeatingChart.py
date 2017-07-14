import random


class SeatingChart:
    # TODO:保存多张座位表
    def __init__(self, m, n):
        self.m = m  # 行数
        self.n = n  # 列数
        self._pos = list(range(len(self)))
        self.names = None  # 名单，初始时为空， name_list[x] => 学号为x的同学的名字
        try:
            self.maintain()
        except FutureWarning:
            print("无法实现自定义规则，将使用随机座位。")

    def __len__(self):
        """返回班上的人数"""
        return self.m * self.n

    def __getitem__(self, i) -> list:
        """返回第i行的同学"""
        return self._pos[i * self.n: (i + 1) * self.n]

    def __str__(self):
        """返回可打印的座位表"""
        s = ''
        for i in range(self.m):
            for j in range(self.n):
                s += str(self[i][j]).rjust(4)
            s += '\n'
        return s

    def index(self, i: int) -> tuple:
        """返回学号为i的同学的位置"""
        i = int(i)
        _real_pos = self._pos.index(i)
        return _real_pos // self.n, _real_pos % self.n

    def get_name(self, i: int, j: int) -> str:
        """返回第i行、第j列同学的名字，没有名单则返回学号"""
        return self.names[self[i][j]] if self.names else str(self[i][j])

    def maintain(self):
        """随机打乱座位表"""
        random.shuffle(self._pos)
        # TODO:处理规则文件

    def load(self, file_name: str):
        """从文件读取名单"""
        with open(file_name) as file:
            names = file.read().split()
            names.insert(0, '空桌子')
            if len(names) >= len(self):
                self.names = names[:len(self)]
            else:
                print("名单长度不足", len(self))

    def save(self, file_name: str):
        """将座位表保存到文件"""
        with open(file_name, 'wt') as file:
            file.write(str(self))
