# cashflow_logic.py

import heapq

class CashFlowMinimizer:

    def __init__(self, names, matrix):  
        self.names = names
        self.matrix = matrix
        self.n = len(names)

    def minimize(self):
        net_balance = [0] * self.n

        for i in range(self.n):
            for j in range(self.n):
                net_balance[i] += self.matrix[i][j] - self.matrix[j][i]

        creditors = []
        debtors = []

        for i in range(self.n):
            if net_balance[i] > 0:
                heapq.heappush(creditors, (-net_balance[i], i))
            elif net_balance[i] < 0:
                heapq.heappush(debtors, (net_balance[i], i))

        result = []

        while creditors and debtors:
            credit, creditor_index = heapq.heappop(creditors)
            debt, debtor_index = heapq.heappop(debtors)

            settled_amount = min(-credit, -debt)

            result.append(
                f"{self.names[debtor_index]} will pay ₹{round(settled_amount, 2)} to {self.names[creditor_index]}"
            )

            remaining_credit = -credit - settled_amount
            remaining_debt = -debt - settled_amount

            if remaining_credit > 0:
                heapq.heappush(creditors, (-remaining_credit, creditor_index))
            if remaining_debt > 0:
                heapq.heappush(debtors, (-remaining_debt, debtor_index))

        return result

