import scipy
import networkx as nx
import numpy as np
from scipy import integrate
import build_network as bn

def disparity_filter(G):
    """
    Implements a case-specialized version of the disparity filter (Serrano, 2009).

    Input:  An undirected weighted graph with edge attributes "common_subreddits" and "weight".
    Return: A disparity filtered, undirected weighted graph with added edge attribute 
            with significance level of each link. 

    References:
    python-backbone-network, https://github.com/aekpalakorn/python-backbone-network
    M. A. Serrano et al. (2009) Extracting the Multiscale backbone of complex weighted networks. PNAS, 106:16, pp. 6483-6488.
    """
    Gdf = nx.Graph()

    for idx, i in enumerate(G):
        if (idx + 1) % 100 == 0:
            print(f"Node {idx+1} of {len(G)}")

        # Node degree
        k = len(G[i])
        if k > 1: # (Serrano 2009, footnote, p. 6485)

            # Node strength:
            s_i = sum( G[i][j]["weight"] for j in G[i])
            for j in G[i]:

                # Disparity Filtering
                w_ij= G[i][j]["weight"]
                p_ij = w_ij / s_i 
                alpha_ij = 1 - (k-1) * scipy.integrate.quad(lambda x: (1-x)**(k-2), 0, p_ij)[0]

                # Saving edge with alpha-value
                Gdf.add_edge(i, j, common_subreddits=G[i][j]["common_subreddits"], weight=w_ij, alpha=alpha_ij)

    return Gdf

def alpha_cut(G, alpha_level=0.05):
    D = nx.Graph()
    for u, v, attributes in G.edges.data(data=True):
        try:
            alpha = attributes["alpha"]
        except KeyError:
            alpha = 1
        
        if alpha < alpha_level:
            cs = attributes["common_subreddits"]
            w = attributes["weight"]
            D.add_edge(u,v, common_subreddits=cs, weight=w)
    return D


if __name__ == "__main__":
    G = nx.read_gpickle("data/networks/w_completeG_no_comments.gpickle")
    print("Initial: Number of nodes: ", len(G.nodes))
    print("Initial: Number of edges: ", len(G.edges))
    
    gw = []
    for u,v, w in G.edges.data(data="weight"):
        gw.append(w)

    # The filtered network exceed github limit by 3 MB so will maybe have to be created
    # once locally.
    #Gdf = disparity_filter(G)
    #nx.write_gpickle(Gdf, "data/networks/w_completeG_disparity_filtered.gpickle")
    Gdf = nx.read_gpickle("data/networks/w_completeG_disparity_filtered.gpickle")
    #print("Filtered: Number of nodes: ", len(Gdf.nodes))
    #print("Filtered: Number of edges: ", len(Gdf.edges))

    # Authors recommend alpha values in the range [0.01, 0.5] (p. 6485)
    alpha_level=0.25
    D = alpha_cut(Gdf, alpha_level=alpha_level)

    path = "data/networks/w_completeD_alpha=" + f"{alpha_level}" + ".gpickle"
    nx.write_gpickle(D, path)

    D = nx.read_gpickle(path)
    print("After alpha_cut(): Number of nodes: ", len(D.nodes))
    print("After alpha_cut(): Number of edges: ", len(D.edges))

    dw = []
    for u,v, w in D.edges.data(data="weight"):
        dw.append(w)

    print(f"Significance level: {alpha_level}")
    print("Percentage of nodes preserved: ", len(D.nodes)/len(G.nodes)*100)
    print("Percentage of edges preserved: ", len(D.edges)/len(G.edges)*100)
    print("Percentage of weight preserved: ", sum(dw) / sum(gw) * 100)

#%%
bn.plot_degree_dist(D, bins=40, weighted=True)

# %%
