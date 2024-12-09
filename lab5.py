from collections import deque

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


V1 = ['a', 'b', 'c']
V2 = ['x', 'y', 'z']
E = [('a', 'x'), ('a', 'y'), ('b', 'y'), ('b', 'z'), ('c', 'z')]

max_matching = find_maximum_matching(V1, V2, E)
print("Максимальное паросочетание:", max_matching)