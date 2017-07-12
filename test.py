import unittest
import random
import SeatingChart


class SeatingChartTestCase(unittest.TestCase):
    def setUp(self):
        m, n = random.randint(1, 100), random.randint(1, 100)
        self.seat = SeatingChart.SeatingChart(m, n)

    def test_rules(self):
        try:
            rules = open('rules.conf')
            for rule in rules:
                if rule == '\n' or rule[0] == '#':
                    continue
                rule = rule.split()
                if rule[0] == 'A':
                    a, b = int(rule[1]), int(rule[2])
                    i, j = self.seat.index(a), self.seat.index(b)
                    self.assertEqual(i[1] ^ 1, j[1], "{}，{}不是同桌".format(a, b))
                elif rule[0] == 'B':
                    a, b = int(rule[1]), int(rule[2])
                    i, j = self.seat.index(a), self.seat.index(b)
                    self.assertNotEqual(i[1] ^ 1, j[1], "{}，{}坐在一起".format(a, b))
                elif rule[0] == 'C':
                    a, i, j = int(rule[1]), int(rule[2]), int(rule[3])
                    pos = self.seat.index(a)
                    self.assertEqual((i, j), pos, "{}不坐在({}, {})".format(a, i, j))
        except (IOError, PermissionError, FileNotFoundError, ValueError):
            print('Cannot open rules.conf')
        finally:
            rules.close()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
