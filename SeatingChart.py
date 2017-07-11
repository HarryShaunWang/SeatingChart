import random


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

    def shuffle(self):
        """随机打乱座位表"""
        random.shuffle(self._pos)
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
        """\
        自定义规则
        A a b ：a, b为同桌
        B a b ：a, b不在一起
        C a i j ：a在第i行第j列，i、j支持通配符
        """
        # TODO:增加支持空座位等

        _MAX_RETRY_TIMES = 1000

        with open("rules.conf", 'r') as rules:
            class RulesError(RuntimeError):
                pass

            try:
                fix = [False] * len(self)
                for rule in rules:  # 处理规则文件
                    if rule == '\n' or rule[0] in ('#',):
                        continue
                    rule = rule.split()
                    if rule[0] == 'A':
                        a, b = int(rule[1]), int(rule[2])
                        i, j = self._pos.index(a), self._pos.index(b)
                        if not (fix[i ^ 1] or fix[j]):
                            self._pos[i ^ 1], self._pos[j] = self._pos[j], self._pos[i ^ 1]
                            fix[i] = fix[i ^ 1] = True
                        else:
                            raise RulesError
                    elif rule[0] == 'B':
                        a, b = int(rule[1]), int(rule[2])
                        i, j = self._pos.index(a), self._pos.index(b)
                        near_by = (i ^ 1, i - self.n, i + self.n)
                        if j in near_by:
                            for cnt in range(_MAX_RETRY_TIMES):
                                k = random.randrange(0, len(self))
                                if k not in near_by and not fix[k]:
                                    self._pos[j], self._pos[k] = self._pos[k], self._pos[j]
                                    fix[i] = fix[k] = True
                                    break
                            else:
                                raise RulesError
                    elif rule[0] == 'C':
                        a = int(rule[1])
                        for cnt in range(_MAX_RETRY_TIMES):
                            i, j = rule[2], rule[3]
                            if i == '*':
                                i = random.randrange(0, self.m)
                            if j == '*':
                                j = random.randrange(0, self.n)
                            i, j = int(i), int(j)
                            pos_ori, pos_new = self._pos.index(a), i * self.n + j
                            if not fix[pos_new]:
                                self._pos[pos_ori], self._pos[pos_new] = self._pos[pos_new], self._pos[pos_ori]
                                fix[pos_ori] = fix[pos_new] = True
                                break
                        else:
                            raise RulesError
            except RulesError:
                print("请检查rules.conf文件")
