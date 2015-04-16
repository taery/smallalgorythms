__author__ = 'taery'


def init_graph(v_count, e_count):
    graph = dict.fromkeys([_ + 1 for _ in range(v_count)])
    for _ in graph:
        graph[_] = []
    for _ in range(e_count):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)
    return graph


def dfs(graph, start):
    used[start] = True
    for v in graph[start]:
        if not used[v]:
            dfs(graph, v)


def count_connected_components(graph):
    used[0] = True
    answer = 0
    while False in used:
        not_used_vertex = used.index(False)
        answer += 1
        dfs(graph, not_used_vertex)
    return answer


def euler_criteria(graph):
    for vertex in graph:
        neighbours_count = len(graph[vertex])
        if neighbours_count % 2 != 0 or neighbours_count == 0:
            return False
    return True


def search_another(graph, neighbours, next_v):
    max_len = len(graph[next_v])
    for _ in neighbours:
        curr_len = len(graph[_])
        if curr_len > max_len:
            max_len = curr_len
            next_v = _
    return next_v


def find_path(graph, vertex):
    neighbours = graph[vertex]
    if len(neighbours) == 0:
        return []
    if vertex in neighbours:
        next_v = vertex
    else:
        next_v = search_another(graph, neighbours, neighbours[0])

    graph[vertex].remove(next_v)
    graph[next_v].remove(vertex)

    vertex__append = [vertex] + find_path(graph, next_v)
    return vertex__append

n, m = map(int, input().split())
g = init_graph(n, m)

used = [False for _ in range(n + 1)]
components = count_connected_components(g)

if not euler_criteria(g) or components > 1:
    print("NONE")
else:
    print(" ".join(map(str, find_path(g, 1))))
