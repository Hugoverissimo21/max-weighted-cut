# %%
import networkx as nx

#G = nx.adjacency_matrix(nx.read_graphml("graphs/04_500.graphml")).todense()
#G

# %% [markdown]
# # exhaustive search
# 
# - ~~recurrence em q  - return max({A...}{...D} , {A...D}{...})~~
# 
# - iterative - compare {A}{...} {AB}{...} ... {A...}{Z}
# 
# penso q ambos seriam 2^n de complexidade pq arvore e n+n-1+n-2+... ?

# %%
import itertools

def exhaustive_search(G):
    input_set = set(range(len(G)))
    subsets = []
    n = len(input_set)
    
    # generate all subsets (complexy 2^V to generate * V to convert to set = O(V^2 * V))
    for r in range(n + 1):
        for subset in itertools.combinations(input_set, r):
            subsets.append(set(subset))

    best = input_set
    weight = 0
    for subset in subsets: # 2^n resultados para percorrer
        new_weight = 0
        for s in subset: # n^2 para calcular o peso
            for t in input_set - subset:
                new_weight += G[s][t]
        if new_weight > weight:
            best = subset
            weight = new_weight
    
    return best, input_set-best, weight

#exhaustive_search(G)

# %% [markdown]
# # greedy heuristic
# 
# pode ser sorted weights e maior é AB, ent S = {A} T = {B}, segudo maior CD, ent S={AC} T={BD}, algo desse genero
# 
# mas se segundo maior é AC - S = {A} T = {BC} :: 
# 
# - if A and C in S or T: pass
# 
# - if A in S or T: C to other
# 
# - if neither in: randomly select - could compare to already in vertices but to complex?
# 
# complexidade nlogn por causa do sort + n por iterar por cada um - logo complexidade final = nlogn ?

# %%
def heuristic_greedy(G):
    num_vertices = len(G)
    
    # Step 1: Extract edges and their weights
    edges = []
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):  # To avoid duplicate edges
            weight = G[i, j]
            edges.append((i, j, weight))

    # Step 2: Sort edges in descending order based on their weights
    edges.sort(key=lambda e: e[2], reverse=True)
    
    seen, S, T = set(), set(), set()

    cut_weight = 0
    # Step 3: Process each edge
    for u, v, weight in edges:
        if u not in seen and v not in seen: 
            # nenhum vertice visto
            cut_weight += weight
            seen.update({u,v})
            S.add(u)
            T.add(v)
        elif u in S and v not in seen:
            # u no primeiro set, v não visto
            cut_weight += weight
            seen.add(v)
            T.add(v)
        elif u in T and v not in seen:
            # u no segundo set, v não visto
            cut_weight += weight
            seen.add(v)
            S.add(v)
        elif v in S and u not in seen:
            # v no primeiro set, u não visto
            cut_weight += weight
            seen.add(u)
            T.add(u)
        elif v in T and u not in seen:
            # v no segundo set, u não visto
            cut_weight += weight
            seen.add(u)
            S.add(u)
        elif v in T and u in S:
            cut_weight += weight
        elif v in S and u in T:
            cut_weight += weight
        # v and u in the same set

    return S, T, cut_weight

#heuristic_greedy(G)


