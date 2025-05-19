# cashflow_logic.py

class CashFlowMinimizer:
    def __init__(self, names, matrix):
        self.names = names
        self.matrix = matrix
        self.n = len(names)

    def minimize(self):
        net = [0] * self.n
        for i in range(self.n):
            for j in range(self.n):
                net[i] += self.matrix[j][i] - self.matrix[i][j]

        result = []

        def get_max_index(arr):
            return arr.index(max(arr))

        def get_min_index(arr):
            return arr.index(min(arr))

        def settle(net):
            max_credit = get_max_index(net)
            max_debit = get_min_index(net)

            if abs(net[max_credit]) < 1e-5 and abs(net[max_debit]) < 1e-5:
                return

            amount = min(-net[max_debit], net[max_credit])
            net[max_credit] -= amount
            net[max_debit] += amount

            result.append(f"{self.names[max_credit]} Will Pay ₹{round(amount, 2)} to {self.names[max_debit]}")
            settle(net)

        settle(net)
        return result
