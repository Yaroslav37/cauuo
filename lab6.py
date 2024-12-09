import numpy as np
from collections import deque

def hungarian_algorithm(C):
    n = len(C)
    alpha = np.zeros(n)
    beta = np.min(C, axis=0)
    
    while True:
        J_eq = set()
        J_lt = set()
        
        for i in range(n):
            for j in range(n):
                if alpha[i] + beta[j] == C[i][j]:
                    J_eq.add((i, j))
                elif alpha[i] + beta[j] < C[i][j]:
                    J_lt.add((i, j))
        
        # Step 4: Find maximum matching in bipartite graph
        V1 = list(range(n))
        V2 = list(range(n, 2*n))
        E = [(i, n+j) for i, j in J_eq]
        M = find_maximum_matching(V1, V2, E)
        
        # Step 5: Check if M is perfect matching
        if len(M) == n:
            return M
        
        # Step 6-10: Update potentials
        reachable_from_s = find_reachable_vertices(V1, V2, E, n)
        I_star = {i for i in range(n) if i in reachable_from_s}
        J_star = {j for j in range(n) if n + j in reachable_from_s}
        
        theta = min(C[i][j] - alpha[i] - beta[j] for i in I_star for j in range(n) if j not in J_star)
        
        for i in range(n):
            if i in I_star:
                alpha[i] += theta
            else:
                alpha[i] -= theta
        
        for j in range(n):
            if j in J_star:
                beta[j] -= theta
            else:
                beta[j] += theta

def build_G_star(V1, V2, E):
    G_star = {v: [] for v in V1 + V2 + ['s', 't']}
    for u, v in E:
        G_star[u].append(v)
    for u in V1:
        G_star['s'].append(u)
    for v in V2:
        G_star[v].append('t')
    return G_star

def bfs(G_star):
    queue = deque(['s'])
    visited = {'s'}
    parent = {'s': None}

    while queue:
        current = queue.popleft()
        if current == 't':
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]
        
        for neighbor in G_star[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    return None

def update_G_star(G_star, path):
    for i in range(1, len(path) - 1):
        u, v = path[i-1], path[i]
        G_star[u].remove(v)
        G_star[v].append(u)

def find_maximum_matching(V1, V2, E):
    G_star = build_G_star(V1, V2, E)
    matching = set()

    while True:
        path = bfs(G_star)
        if not path:
            for v in V2:
                for u in G_star[v]:
                    if u in V1:
                        matching.add((u, v))
            return matching
        
        update_G_star(G_star, path)

def find_reachable_vertices(V1, V2, E, n):
    G_star = build_G_star(V1, V2, E)
    reachable = set()
    queue = deque(['s'])
    visited = {'s'}

    while queue:
        current = queue.popleft()
        reachable.add(current)
        for neighbor in G_star[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return reachable

# Example usage
C = [
    [7, 2, 1, 9, 4],
    [9, 6, 9, 5, 5],
    [3, 8, 3, 1, 8],
    [7, 9, 4, 2, 2],
    [8, 4, 7, 4, 8]
]

result = hungarian_algorithm(C)
print("Оптимальное решение задачи о назначениях:", result)