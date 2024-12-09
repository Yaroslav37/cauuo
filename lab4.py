FROM = 0
TO = 3
GRAPH = [
    [ (1, 4),   (4, 2)  ],
    [ (2, 10),  (4, 5)  ],
    [ (3, 11)   ],
    [],
    [ (5, 3)    ],
    [ (2, 4)    ]
]


def _gsort(graph, current_vertex, states):
    
    if states[current_vertex] == 1:
        raise Exception("Graph has a loop!")
    
    states[current_vertex] = 1
    result = []

    for vertex, _ in graph[current_vertex]:
        if states[vertex] != 2:
            result = _gsort(graph, vertex, states) + result
    
    states[current_vertex] = 2
    
    return [ current_vertex ] + result


def gsort(graph, from_vertex):
    states = [ 0 ] * len(graph)
    
    return _gsort(graph, from_vertex, states)


def _longest_path(graph, gsorted, gsorted_from, gsorted_to):
    vertex_count = gsorted_to - gsorted_from

    if vertex_count == 0:
        return 0, [ gsorted[gsorted_from] ]

    available_verteces = { gsorted[gsorted_to] : (gsorted[gsorted_to], 0) } # map of pairs (second_vertex, length)

    while gsorted_to > gsorted_from:
        gsorted_to -= 1
        
        best_vertex = gsorted[gsorted_to]
        best_length = 0

        for vertex, length in graph[gsorted[gsorted_to]]:
            if vertex in available_verteces:
                potential_best_length = available_verteces[vertex][1] + length
                if potential_best_length > best_length:
                    best_vertex = vertex
                    best_length = potential_best_length
        
        if best_length > 0:
            available_verteces[gsorted[gsorted_to]] = (best_vertex, best_length)

    starting_vertex = gsorted[gsorted_from]

    if starting_vertex not in available_verteces:
        raise Exception("Cannot get to the destination")
    
    path = [ starting_vertex ]

    while available_verteces[starting_vertex][0] != starting_vertex:
        starting_vertex = available_verteces[starting_vertex][0]
        path.append(starting_vertex)
    
    return best_length, path


def longest_path(graph, gsorted, from_vertex, to_vertex):
    
    for i, vertex in enumerate(gsorted):
        if vertex == from_vertex:
            gsorted_from = i
            break
        if vertex == to_vertex:
            raise Exception("Cannot get to the destination")
    
    for i, vertex in enumerate(gsorted, i):
        if vertex == to_vertex:
            gsorted_to = i
            break
    
    try:
        return _longest_path(graph, gsorted, gsorted_from, gsorted_to)
    except UnboundLocalError:
        raise Exception("Cannot get to the destination")
        

def main():
    gsorted = gsort(GRAPH, FROM)
    print(longest_path(GRAPH, gsorted, FROM, TO))


if __name__ == "__main__":
    main()