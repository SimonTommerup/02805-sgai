import pandas as pd
import numpy as np
import re
import nltk
import networkx as nx
import matplotlib.pyplot as plt
import json

from collections import Counter
from tqdm import tqdm

# %%
def plot_degree_dist(G, bins, weighted):
    if weighted:
        degrees = [val for (node, val) in G.degree(weight='weight')]
    else: 
        degrees = [val for (node, val) in G.degree()]


    k_min = np.min(degrees)
    k_max = np.max(degrees)
    print(f"k_min: {min(degrees)}, k_max: {max(degrees)}")
    count, bins = np.histogram(degrees, bins=bins)
    plt.subplots(figsize=(10,8))  

    # Hist plot
    #plt.hist(bins[:len(bins)-1], count, color="darksalmon")
    plt.hist(degrees, bins, color="darkslategray")

    plt.title("Histogram of the degree distrubution ")   
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.show()


def get_ids_of_users_with_common_subreddits(user_id, users, used_subreddits):
    users_with_common_subreddits = []
    for other_user_id in range(len(users)):
        if other_user_id != user_id:  # Skip connection to self
            for subr in used_subreddits[user_id]:
                if subr in used_subreddits[other_user_id]:
                    users_with_common_subreddits.append(other_user_id)
                    break
    return users_with_common_subreddits


def get_common_subreddits(user_id, other_user_id, used_subreddits):
    common_subreddits = [subreddit for subreddit in used_subreddits[user_id] if subreddit in used_subreddits[other_user_id]]
    return common_subreddits


def load_data(file, main_reddits):
    # ['user', 'from_subreddit', 'comment', 'used_subreddits', 'comment_sentiment']
    df = pd.read_csv(file, sep=";")
    used_subreddits = np.array(df.used_subreddits)
    users = np.array(df.user)
    from_subreddit = np.array(df.from_subreddit)


    used_subreddits_list = []
    for i, l in enumerate(used_subreddits):
        # l1 = re.findall(r"\'(.*?)\'[,\]]", l) # TODO: Decode using json instead!
        l1 = json.loads(l)
        # if main_reddits[0] in l1:
        #     l1.remove(main_reddits[0])
        # if main_reddits[1] in l1:
        #     l1.remove(main_reddits[1])
        used_subreddits_list.append(l1)
    
    return users, used_subreddits_list, from_subreddit


def get_subreddits_common_for_both(from_subreddits, used_subreddits, main_reddits):
    all_subreddits_trump = []
    all_subreddits_biden = []

    for i, user_subreddits in enumerate(used_subreddits):
        user_unique_subreddits = list(set(user_subreddits)) # Removes possible duplicates
        if from_subreddits[i] == main_reddits[0]:
            all_subreddits_trump += user_unique_subreddits
        elif from_subreddits[i] == main_reddits[1]:
            all_subreddits_biden += user_unique_subreddits

    # Trump
    counts = Counter(all_subreddits_trump)
    tf_trump = {n: c for n, c in counts.items()}

    # Biden 
    counts = Counter(all_subreddits_biden)
    tf_biden = {n: c for n, c in counts.items()}


    # _____METHOD 1________: TFTR 
    c = 10
    all_subreddits = list(set(list(tf_trump.keys()) + list(tf_biden.keys())))
    TFTR = []
    TFTR_raw = []

    for subreddit in all_subreddits:
        if subreddit in tf_biden:
            biden_f = tf_biden[subreddit]
        else:
            biden_f = 0

        if subreddit in tf_trump:
            trump_f = tf_trump[subreddit]
        else:
            trump_f = 0

        weight = max(trump_f, biden_f)/(min(trump_f, biden_f)+c)
        TFTR.append((subreddit, weight))
        TFTR_raw.append([subreddit, trump_f+biden_f, weight, "trump" if trump_f > biden_f else "biden"])
        TFTR_dict = {n: c for n, c in TFTR}


    # _____METHOD 2________: Abs(freq) threshold + relative
    # rel_difs = []
    # ignore = []
    # c = 1
    # all_subreddits = [tf_trump.keys()] + [tf_biden.keys()]
    # for subreddit, trump_f in tf_trump.items():
    #     #if subreddit in tf_biden:
    #         # if trump_f < min_comments and biden_f < min_comments:  # Ignore if only X user ever commented
    #         #     ignore.append(subreddit)
    #         # else:
    #     biden_f = tf_biden[subreddit]
    #     fraction = min(trump_f, biden_f)/max(trump_f, biden_f)

    #     if (1-fraction) > threshold:  # If one has threshold% more comments on subreddit than other
    #         rel_difs.append([subreddit,
    #                         (1 - fraction),
    #                         "trump" if trump_f>biden_f else "biden"])
    #     else:
    #         ignore.append(subreddit)
    

    # ___________METHOD 3: ASSIGN WEIGHTS OPPOSITE TFTR
    # subreddit_weights = []
    # ignore = []
    # c = 1
    # all_subreddits = [tf_trump.keys()] + [tf_biden.keys()]
    # for subreddit in all_subreddits:
    #     if subreddit in tf_biden:
    #         biden_f = tf_biden[subreddit]
    #     else:
    #         biden_f = 0

    #     if subreddit in tf_trump:
    #         trump_f = tf_trump[subreddit]
    #     else:
    #         trump_f = 0

    #     fraction = (min(trump_f, biden_f)+c)/max(trump_f, biden_f)
    #     subreddit_weights.append(fraction)

    return TFTR_dict, TFTR_raw


def create_graph(users, used_subreddits, from_subreddits, n_required_subreddits=1):
    G = nx.Graph()
    # Loop through all users
    for user_id in tqdm(range(len(users))):
        # Add a node for EVERY user in data set 
        G.add_node(users[user_id], from_subreddit=from_subreddits[user_id])

        # Get all other users with atleast one other subreddit in common
        other_users_id = get_ids_of_users_with_common_subreddits(user_id, users, used_subreddits)
        for other_user_id in other_users_id:
            # Save all UNIQUE common subreddits as edge property if constraints satisfied
            common_subreddits = get_common_subreddits(user_id, other_user_id, used_subreddits)
            common_subreddits = list(set(common_subreddits))
            # Remove potentiel 'from_subreddit' as common subreddit
            common_subreddits = list(filter(lambda e: e not in from_subreddits[user_id], common_subreddits))  
            if len(common_subreddits) >= n_required_subreddits:
                G.add_edge(users[user_id], users[other_user_id], common_subreddits=(common_subreddits), 
                           weight=len(common_subreddits))

    return G

def add_weights_to_graph(G, w_dict):
    G_w = nx.Graph()


    for u, v, common_subreddits in G.edges.data(data='common_subreddits'):
        w = 0
        for c_subreddit in common_subreddits:
            w += w_dict[c_subreddit]
            G_w.add_edge(u, v, common_subreddits=common_subreddits, weight=w)

    return G_w



# %%


#main_reddits = ['President Donald Trump - Trump 2020! - Election Defense Task Force - Stop The Steal!', 
              #  "President-elect Joe Biden"]

main_reddits = ['trump', 'biden']

# Load data
users, used_subreddits, from_subreddits = load_data("./data/csv_files/data_partitions_all.csv", main_reddits)
from_subreddits = ["trump" if "trump" in s.lower() else "biden" for s in from_subreddits]

#for i in range(len(used_subreddits))

# Create graph
# TODO: Tildel vægte = Antal fælles reddits! Bevarer info + betydning bevares. 
G = create_graph(users, used_subreddits, from_subreddits, n_required_subreddits=5)
#%%

# Create weighted graph
w_dict, TFTR_raw = get_subreddits_common_for_both(from_subreddits, used_subreddits, main_reddits)
w_list = sorted(list(w_dict.items()), key=lambda x: x[1])
#G_w = add_weights_to_graph(G, w_dict)

# Plot degree dist
plot_degree_dist(G, bins=50, weighted=False)


# Save graph
#nx.write_gpickle(G, "./data/networks/test.gpickle")

# Load graph
#H = nx.read_gpickle("./data/networks/test.gpickle")






###### CHECK DATA IN GRAPH #########
lis = [n for n in G.nodes if G.nodes[n]['from_subreddit'] == main_reddits[1]]

ws = []
for u, v, w in G.edges.data(data="weight"):
    ws.append(w)
ws = sorted(ws)



## Degrees
degrees_w = [val for (node, val) in G.degree(weight='weight')]
degrees = [val for (node, val) in G.degree()]
degrees.sort()
degrees_w.sort()


## Freq dists of reddits
res = sorted(TFTR_raw, key=lambda x: x[1])
freq_but_not_dif = [[r, f, w, c] for r, f, w, c in res if w > 0.75 and w < 1.25 and f > 30]
# %%
