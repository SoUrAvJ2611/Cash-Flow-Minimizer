# cashflow_logic.py

class CashFlowMinimizer:
    def __init__(self, names, matrix):  # fixed constructor
        self.names = names
        self.matrix = matrix
        self.n = len(names)

    def minimize(self):
        net_balance = [0] * self.n
        for i in range(self.n):
            for j in range(self.n):
                net_balance[i] += self.matrix[j][i] - self.matrix[i][j]

        creditors = []
        debtors = []
        for i in range(self.n):
            if net_balance[i] > 0:
                creditors.append((i, net_balance[i])) 
            elif net_balance[i] < 0:
                debtors.append((i, -net_balance[i]))

        result = []
        i, j = 0, 0
        while i < len(creditors) and j < len(debtors):
            creditor_index, credit = creditors[i]
            debtor_index, debt = debtors[j]
            settled_amount = min(credit, debt)

            result.append(
                f"{self.names[creditor_index]} will pay ₹{round(settled_amount, 2)} to {self.names[debtor_index]}"
            )

            creditors[i] = (creditor_index, credit - settled_amount)
            debtors[j] = (debtor_index, debt - settled_amount)

            if creditors[i][1] == 0:
                i += 1
            if debtors[j][1] == 0:
                j += 1

        return result
