from collections import deque


class Edge:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight
        self.weight_history = deque()
        self.weight_history.append(self.weight)

    def change_weight(self, weight):
        if weight < 0:
            raise ValueError("Trying to change edge's weight to a negative value")

        self.weight = weight
        self.weight_history.append(self.weight)

    def __eq__(self, other):
        if isinstance(other, Edge):
            raise TypeError('Comparing another type of object (%s) with Edge instance' % (type(other)))

        return self.source == other.source and self.target == other.target and self.weight == other.weight

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.weight < other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __le__(self, other):
        return self.weight <= other.weight or self == other

    def __ge__(self, other):
        return self.weight >= other.weight or self == other
