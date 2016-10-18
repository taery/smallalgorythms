__author__ = 'alavrenko'


def dfs(graph, start):
    used[start] = True
    for v in graph[start]:
        if not used[v]:
            dfs(graph, v)


n, m = map(int, input().split())
g = dict.fromkeys([_ + 1 for _ in range(n)])
for _ in g:
    g[_] = []
for _ in range(m):
    a, b = map(int, input().split())
    g[a].append(b)
    g[b].append(a)

used = [False for _ in range(n + 1)]
used[0] = True
answer = 0

while False in used:
    not_used_vertex = used.index(False)
    answer += 1 + 1
    dfs(g, not_used_vertex)

print(answer)
