from collections import defaultdict
import heapq


# Function to find the root of a node in a disjoint set with path compression
def find(parent, i):
    if parent[i] == i:
        return i
    parent[i] = find(parent, parent[i])
    return parent[i]


# Function to union two sets by rank
def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)
    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1


# Kruskal's algorithm for finding the MST
def kruskalMST(graph):
    mst = []
    edges = graph['edges']
    edges.sort(key=lambda x: x[2])
    parent = list(range(graph['V']))
    rank = [0] * graph['V']

    def find(parent, i):
        if parent[i] == i:
            return i
        parent[i] = find(parent, parent[i])
        return parent[i]

    def union(parent, rank, x, y):
        xroot = find(parent, x)
        yroot = find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    for u, v, w in edges:
        x = find(parent, ord(u) - ord('a'))
        y = find(parent, ord(v) - ord('a'))
        if x != y:
            mst.append((u, v, w))
            union(parent, rank, x, y)
            if len(mst) == graph['V'] - 1:
                break

    return mst


# Example usage for Kruskal's algorithm
graph_kruskal = {
    'V': 6,
    'edges': [
        ('a', 'b', 4), ('a', 'c', 2), ('b', 'c', 3),
        ('b', 'd', 6), ('b', 'f', 5), ('c', 'd', 7),
        ('c', 'e', 8), ('d', 'e', 9), ('d', 'f', 10)
    ]
}

print("Kruskal's MST:")
mst = kruskalMST(graph_kruskal)
print("The final MST edges highlighted are:", mst)
total_weight = sum(w for u, v, w in mst)
print(f"Total weight: {total_weight}")


# Prim's algorithm for finding the MST
def primMST(graph, vertex_map):
    mst = []
    key = [float('inf')] * len(vertex_map)
    parent = [None] * len(vertex_map)
    key[0] = 0
    heap = [(0, 0)]  # (weight, vertex_index)

    while heap:
        w, u = heapq.heappop(heap)
        if key[u] < w:
            continue
        u_vertex = list(vertex_map.keys())[list(vertex_map.values()).index(u)]
        parent_vertex = None if parent[u] is None else list(vertex_map.keys())[
            list(vertex_map.values()).index(parent[u])]
        mst.append((u_vertex, parent_vertex, w))

        for v, weight in graph['adj'][u_vertex]:
            v_index = vertex_map[v]
            if weight < key[v_index]:
                key[v_index] = weight
                parent[v_index] = u
                heapq.heappush(heap, (weight, v_index))

    return mst


# Example usage for Prim's algorithm
graph_prim = {
    'V': 9,
    'edges': [
        ('a', 'b', 4), ('a', 'h', 8), ('b', 'c', 8),
        ('b', 'h', 11), ('c', 'd', 7), ('c', 'f', 4),
        ('c', 'i', 2), ('d', 'e', 9), ('d', 'f', 14),
        ('e', 'f', 10), ('f', 'g', 2), ('g', 'h', 1),
        ('g', 'i', 6), ('h', 'i', 7)
    ],
    'adj': defaultdict(list)
}

# Add edges to the adjacency list
for u, v, w in graph_prim['edges']:
    graph_prim['adj'][u].append((v, w))
    graph_prim['adj'][v].append((u, w))

vertex_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}

print("\nPrim's MST:")
mst = primMST(graph_prim, vertex_map)
print("The final MST edges highlighted are:", mst)
total_weight = sum(w for u, parent, w in mst if parent is not None)
print(f"Total weight: {total_weight}")
