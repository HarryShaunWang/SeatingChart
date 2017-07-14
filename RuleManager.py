RULES_FILE = 'rules.conf'


class Rule:
    """规则基类"""

    def __init__(self):
        self.origin = None
        self.target = None


class RuleA(Rule):
    """同桌规则"""
    pass


class RuleB(Rule):
    """疏远规则"""
    pass


class RuleC(Rule):
    """指定位置规则"""
    pass


class RuleManager:
    """规则管理器，一个管理器对应一组规则"""

    def __init__(self):
        pass

    def __str__(self):
        """返回自然语言描述的规则"""
        pass

    def __repr__(self):
        """返回文本形式的规则"""
        pass

    def add_rule(self, rule: Rule, pos=None):
        pass

    def del_rule(self, pos=None):
        pass

    def new_rule(self, *args, **kwargs):
        pass

    def commit(self, file_name=RULES_FILE):
        """Save"""
        pass

    def reload(self):
        """Load"""
        pass


def get_rules() -> RuleManager:
    pass
