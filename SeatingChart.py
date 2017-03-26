#!/usr/bin/env python
class SeatingChart:
    """座位表"""

    def __init__(self, m, n):
        """座位一共有m行，n列"""
        self.m = m
        self.n = n
        self._pos = [x for x in range(len(self))]
        self.shuffle()

    def __str__(self):
        """返回一张可视化的座位表"""
        s = ''
        for i in range(self.m):
            for j in range(self.n):
                s += str(self[i][j]).rjust(4)
            s += '\n'
        return s

    def __len__(self):
        """返回座位表中的总人数"""
        return self.m * self.n

    def __getitem__(self, i):
        """获取第i行的同学的列表"""
        return self._pos[i * self.n: (i + 1) * self.n]

    def shuffle(self):
        """打乱座位表"""
        from random import shuffle
        shuffle(self._pos)
        self.maintain()  # 恢复自定义规则

    def maintain(self):
        """一些自定义规则"""
        from random import randrange
        tmp = self[1][randrange(0, self.n)]
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
