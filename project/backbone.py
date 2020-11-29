import scipy
import networkx as nx
import numpy as np
from scipy import integrate
import build_network as bn
import matplotlib.pyplot as plt

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
    """
    Implements the removal of edges in G that are not significant on alpha_level.
    References: 
    python-backbone-network, https://github.com/aekpalakorn/python-backbone-network
    M. A. Serrano et al. (2009) Extracting the Multiscale backbone of complex weighted networks. PNAS, 106:16, pp. 6483-6488.
    """
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

def local_heterogeneity(G):
    nodes_by_ascending_degree = sorted(G.degree, key=lambda x: x[1], reverse=False)
    upsilon = []
    degrees = []
    for tup in nodes_by_ascending_degree:
        i = tup[0]
        k = tup[1]
        degrees.append(k)

        # Calculate sum of weights of incident edges
        s_i = sum(G[i][j]["weight"] for j in G[i])

        # Calculate square on each normalized weight
        pij_sq = [ (G[i][j]["weight"] / s_i)**2 for j in G[i]]

        # Sum of the squares:
        sum_pij_sq = sum(pij_sq)

        # Upsilon(i, k)
        upsilon.append( k * sum_pij_sq )
    
    return upsilon, degrees

if __name__ == "__main__":

#%%
    G = nx.read_gpickle("data/networks/G_weighted_T_B_removed.gpickle")
    gw = []
    for u, v, weight in G.edges.data(data="weight"):
        gw.append(weight)

    gw2 = [val for (node, val) in G.degree(weight='weight')]

    plt.hist(gw2, bins=20)
    plt.show()



    Ntot = len(G.nodes)
    Ltot = len(G.edges)
    # The filtered network exceed github limit by 3 MB so will maybe have to be created
    # once locally by running: Gdf = disparity_filter(G)
    #Gdf = disparity_filter(G)
    #nx.write_gpickle(Gdf, "data/networks/G_disparity_filtered.gpickle")

    Gdf = nx.read_gpickle("data/networks/G_disparity_filtered.gpickle")


#%%
    # Authors recommend alpha values in range [0.01, 0.5]
    alpha_levels = np.arange(0.01, 0.51, 0.01)

    xvals = []
    yvals = []
    for idx, alpha_level in enumerate(alpha_levels):
        print(idx+1)
        D = alpha_cut(Gdf, alpha_level=alpha_level)

        Np = len(D.nodes)
        Lp = len(D.edges)

        yvals.append(Np / Ntot)
        xvals.append(Lp / Ltot)


    # Authors recommend alpha values in range [0.01, 0.5]
    alpha_levels = np.arange(0.01, 0.51, 0.01)
    tw = []
    for u, v, weight in G.edges.data(data="weight"):
        tw.append(weight)

    total_weight = sum(tw)

    xvals = []
    yvals = []
    for idx, alpha_level in enumerate(alpha_levels):
        print(idx+1)
        D = alpha_cut(Gdf, alpha_level=alpha_level)

        Np = len(D.nodes)
        Lp = len(D.edges)

        dw = []
        for u, v, weight in D.edges.data(data="weight"):
            dw.append(weight)

        yvals.append(Np / Ntot)
        xvals.append(sum(dw) / total_weight)



    # %%

    plt.plot(xvals, yvals, 'bo')
    plt.plot(xvals[8], yvals[8], 'ro')
    plt.title("Fraction of preserved nodes as function of fraction of preserved weight")
    plt.xlabel("Lp / Ltot")
    plt.ylabel("Np / Ntot")
    plt.show()
    # %%

    plt.plot(alpha_levels, yvals, 'o', color="darksalmon")
    plt.plot(alpha_levels, xvals, 'o', color="deepskyblue")
    plt.plot(np.arange(0.0, 0.5,0.01), np.arange(0.0, 0.5,0.01), 'o', color="darkslategray")
    plt.title("Fraction of preserved nodes and preserved edges as function of alpha")
    plt.xlabel("alpha")
    plt.ylabel("Np / Ntot")
    plt.show()


#%%

    res = [x / y for x, y in zip(xvals, yvals)]
    print(np.argmax(res))

    print(res)

# %%

print(alpha_levels[8])

print(xvals)
# %%
print(yvals)
# %%

lst=[]
for x, y in zip(xvals, yvals):
    lst.append(y/x)

print(np.argmax(lst))


# %%


B = alpha_cut(Gdf, alpha_level=0.09)
nx.write_gpickle(B, "data/networks/BackBone_alpha=0.09.gpickle")