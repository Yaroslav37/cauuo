import numpy as np

def allocate_resources(A, Q, P):
    B = np.zeros((P + 1, Q + 1), dtype=int)
    C = np.zeros((P + 1, Q + 1), dtype=int)
    
    for p in range(1, P + 1):
        for q in range(Q + 1):
            if p == 1:
                B[p][q] = A[p-1][q]
                C[p][q] = q
            else:
                max_profit = 0
                best_i = 0
                for i in range(q + 1):
                    current_profit = A[p-1][i] + B[p-1][q-i]
                    if current_profit > max_profit:
                        max_profit = current_profit
                        best_i = i
                B[p][q] = max_profit
                C[p][q] = best_i

    allocation = []
    q = Q
    for p in range(P, 0, -1):
        allocation.append(int(C[p][q]))
        q -= C[p][q]
    allocation.reverse()
    
    max_profit = B[P][Q]
    
    return max_profit, allocation

A = [
    [0, 1, 2, 3],
    [0, 0, 1, 2],
    [0, 2, 2, 3]
]
Q = 3
P = 3

max_profit, allocation = allocate_resources(A, Q, P)
print("Максимальная прибыль:", max_profit)
print("Распределение ресурсов по агентам:", allocation)
