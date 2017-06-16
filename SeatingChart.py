def maintain(seats: list, m: int, n: int):
    """自定义规则"""
    from random import randrange
    i, j, tmp = seats.index(20), seats.index(26), 8 + randrange(0, n)
    seats[i], seats[tmp] = seats[tmp], seats[i]
    i = tmp
    seats[j], seats[i ^ 1] = seats[i ^ 1], seats[j]

    i, j = seats.index(0), seats.index(7)
    seats[i], seats[j ^ 1] = seats[j ^ 1], seats[i]


class SeatingChart:
    """m行n列的座位表"""

    def __init__(self, m, n):
        self.m = m  # 行数
        self.n = n  # 列数
        self._pos = list(range(len(self)))
        self.names = []  # 名单，初始时为空， name_list[x] => 学号为x的同学的名字
        self.shuffle()

    def __len__(self):
        """返回班上的总座位数"""
        return self.m * self.n

    def __getitem__(self, i) -> list:
        """获取第i行的同学"""
        items = self._pos[i * self.n: (i + 1) * self.n]
        return [self.get_name(x) for x in items]

    def __str__(self):
        """返回可打印的座位表"""
        s = ''
        for i in range(self.m):
            for j in range(self.n):
                s += self[i][j].rjust(4)
                if j % 2 == 1 and j + 1 != self.n:
                    s += '||'
            s += '\n'
        return s

    def get_name(self, i: int) -> str:
        """获得第i个同学的名字，没有名单则返回学号"""
        return self.names[i] if self.names else str(i)

    def shuffle(self):
        """随机打乱座位表"""
        from random import shuffle
        shuffle(self._pos)
        maintain(self._pos, self.m, self.n)  # 恢复自定义规则

    def set_names(self, names: list):
        """"设置班级名单"""
        names.insert(0, '空桌子')
        if len(names) >= len(self):
            self.names = names[0: len(self)]
        else:
            raise ValueError("名单长度不足{num}".format(num=len(self)))

    def load(self, file_name: str):
        """从文件读取名单"""
        file = open(file_name, 'rt')
        try:
            names = file.read().split()
            self.set_names(names)
        except IOError:
            print('IOError')
        except PermissionError:
            print('PermissionError')
        finally:
            file.close()

    def save(self, file_name: str):
        """将座位表保存到文件"""
        file = open(file_name, 'wt')
        try:
            file.write(str(self))
        except IOError:
            print('IOError')
        except PermissionError:
            print('PermissionError')
        finally:
            file.close()
