class Edge:
    def __init__(self, ID: int, _from: int, to: int, cost: int):
        self.ID = ID
        self._from = _from
        self.to = to
        self.cost = cost