class SeatingChart:
    # TODO:保存多张座位表
    def __init__(self, m, n):
        self.m = m  # 行数
        self.n = n  # 列数
        self._pos = list(range(len(self)))
        self.names = None  # 名单，初始时为空， name_list[x] => 学号为x的同学的名字
        self.shuffle()

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
                s += self[i][j].rjust(4)
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

    def shuffle(self):
        """随机打乱座位表"""
        from random import shuffle
        shuffle(self._pos)
        self.maintain()  # 恢复自定义规则

    def load(self, file_name: str):
        """从文件读取名单"""
        file = open(file_name, 'r')
        try:
            names = file.read().split()
            names.insert(0, '空桌子')
            if len(names) >= len(self):
                self.names = names[:len(self)]
            else:
                raise ValueError
        except IOError:
            print('IOError')
        except PermissionError:
            print('PermissionError')
        except ValueError:
            print("名单长度不足", len(self))
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

    def maintain(self):
        """自定义规则"""

        # TODO:将规则独立到文件，支持同桌，疏远，指定位置，空座位等
        # TODO:需要一个GUI规则编辑器

        def _mk_deskmate(student_a: int, student_b: int):
            """把 a 的同桌变成 b"""
            pos_a, pos_b = self._pos.index(student_a), self._pos.index(student_b)
            self._pos[pos_a ^ 1], self._pos[pos_b] = self._pos[pos_b], self._pos[pos_a ^ 1]

        from random import randrange
        tmp = self[1][randrange(0, self.n)]
        _mk_deskmate(tmp, 20)
        _mk_deskmate(20, 26)
        del tmp

        _mk_deskmate(7, 0)
