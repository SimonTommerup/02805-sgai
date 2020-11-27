import networkx as nx
import sys
sys.path.insert(0, "./../project/")

import backbone

G = nx.read_gpickle("../project/data/networks/w_completeG_no_comments.gpickle")
print(len(G.nodes))

N = len(G.nodes)

Lmax = N*(N-1)/2

print("Lmax = ", Lmax)

L = len(G.edges)

pct = L / Lmax 
Gdf = nx.read_gpickle("../project/data/networks/w_completeG_disparity_filtered.gpickle")
print("Percent of Lmax: ", pct)
D = backbone.alpha_cut(Gdf)
#%%
print(len(D.edges))
# %%
