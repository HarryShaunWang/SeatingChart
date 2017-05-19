class SeatingChart:
    def __init__(self, m, n):
        self.m = m  # 行数
        self.n = n  # 列数
        self._pos = list(range(len(self)))
        self.names = []  # 名单，初始时为空， name_list[x] => 学号为x的同学的名字
        self.shuffle()

    def __len__(self):
        return self.m * self.n

    def __getitem__(self, i):
        """获取第i行的同学的列表"""
        items = self._pos[i * self.n: (i + 1) * self.n]
        return [self.get_name(x) for x in items]

    def __str__(self):
        """返回可视化的座位表"""
        s = ''
        for i in range(self.m):
            for j in range(self.n):
                s += self[i][j].rjust(4)
                if j % 2 == 1 and j + 1 != self.n:
                    s += '||'
            s += '\n'
        return s

    def get_name(self, i):
        return self.names[i] if self.names else str(i)

    def shuffle(self):
        """随机打乱座位表"""
        from random import shuffle
        shuffle(self._pos)
        self.maintain()  # 恢复自定义规则

    def maintain(self):
        """自定义规则"""
        from random import randrange
        tmp = self._pos[8:16][randrange(0, self.n)]
        self.swap_num(20, tmp)
        self.swap_num(26, self.desk_mate(20))
        self.swap_num(0, self.desk_mate(7))

    def desk_mate(self, x):
        """返回学号为x的同桌的学号"""
        return self._pos[self._pos.index(x) ^ 1]

    def swap_num(self, x, y):
        """交换学号为x， y的两名同学的位置"""
        i, j = self._pos.index(x), self._pos.index(y)
        self._pos[i], self._pos[j] = self._pos[j], self._pos[i]

    def set_name(self, names):
        """"设置班级名单"""
        names.insert(0, '空桌子')
        if len(names) >= len(self):
            self.names = names[0: len(self)]
        else:
            raise ValueError("名单长度不足{num}".format(num=len(self)))

    def load(self, file_name):
        """从文件读取名单"""
        with open(file_name) as file:
            names = file.read().split()
            self.set_name(names)

    def save(self, file_name):
        """将座位表保存到文件"""
        with open(file_name, 'w') as file:
            file.write(str(self))
