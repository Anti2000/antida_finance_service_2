from collections import defaultdict
from decimal import Decimal


class OperationReport:
    def __init__(self, name: str) -> None:
        self.name = name
        self.amounts = defaultdict(Decimal)
        self.total_amounts = Decimal(0.0)
        self.children = {}

    def add_row(self, operation, path: list[str]):
        operation_total_price = round(Decimal(operation.amount) * Decimal(operation.price), 2)
        self.amounts[operation.date] += operation_total_price
        self.total_amounts += operation_total_price

        if path:
            key = path.pop(0)
            try:
                child = self.children[key]
            except KeyError:
                child = self.children[key] = OperationReport(key)
            child.add_row(operation, path)
