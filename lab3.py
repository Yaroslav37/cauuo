def knapsack(values, weights, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    max_value = dp[n][capacity]

    w = capacity
    items_selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            items_selected.append(i - 1)
            w -= weights[i - 1]

    return max_value, items_selected

values = [10, 40, 30]
weights = [5, 4, 6]
capacity = 10

max_profit, items = knapsack(values, weights, capacity)
print("Максимальная ценность:", max_profit)
print("Выбранные предметы (по индексу):", items)
