class Condition:
    def __init__(self, key: str, comparator: str='>=', value=1):
        self.key = key
        self.comparator = comparator
        self.value = value

    def evaluate(self, data: dict) -> bool:
        if self.key == None:
            return True
        if self.key not in data:
            return False
        value = data[self.key]
        if self.comparator == '==':
            return value == self.value
        elif self.comparator == '!=':
            return value != self.value
        if self.comparator == '>':
            return value > self.value
        if self.comparator == '<':
            return value < self.value
        if self.comparator == '>=':
            return value >= self.value
        if self.comparator == '<=':
            return value <= self.value
        else:
            raise ValueError(f"Unsupported comparator: {self.comparator}")
    def __and__(self, other):
        if isinstance(other, Condition):
            other = CompositeCondition('and', [other])
        return CompositeCondition('and', [self, other])
    def __or__(self, other):
        if isinstance(other, Condition):
            other = CompositeCondition('or', [other])
        return CompositeCondition('or', [self, other])
    def __invert__(self):
        return CompositeCondition('not', [self])

class CompositeCondition:
    def __init__(self, operator, conditions):
        self.operator = operator
        self.conditions = conditions

    def evaluate(self, data: dict) -> bool:
        if self.operator == 'and':
            return all(cond.evaluate(data) for cond in self.conditions)
        elif self.operator == 'or':
            return any(cond.evaluate(data) for cond in self.conditions)
        elif self.operator == 'not':
            return not self.conditions[0].evaluate(data)
        else:
            raise ValueError(f"Unsupported operator: {self.operator}")

    def __and__(self, other):
        if isinstance(other, Condition):
            other = CompositeCondition('and', [other])
        return CompositeCondition('and', [self, other])

    def __or__(self, other):
        if isinstance(other, Condition):
            other = CompositeCondition('or', [other])
        return CompositeCondition('or', [self, other])

    def __invert__(self):
        return CompositeCondition('not', [self])

if __name__ == '__main__':
    cond1 = Condition('age', '>=', 18)
    cond2 = Condition('country', '==', 'China')
    cond3 = Condition('is_student', '==', True)

    # 构建复合条件
    comp_cond = (cond1 & (cond2 | cond3))  # (age >= 18) and ((country == 'China') or (not is_student))

    # 评估复合条件
    data1 = {'age': 20, 'country': 'China', 'is_student': True}
    data2 = {'age': 16, 'country': 'USA', 'is_student': False}

    print(comp_cond.evaluate(data1))  # 输出: True
    print(comp_cond.evaluate(data2))  # 输出: False