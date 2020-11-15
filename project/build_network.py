import pandas as pd
import numpy as np
import re
import nltk
import networkx as nx
import matplotlib.pyplot as plt
import json

from collections import Counter
from tqdm import tqdm


def plot_degree_dist(G):
    degrees = [val for (node, val) in G.degree()]

    k_min = np.min(degrees)
    k_max = np.max(degrees)
    print(f"k_min: {min(degrees)}, k_max: {max(degrees)}")
    count, bins = np.histogram(degrees, bins=k_max//4)
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
        # used_subreddits_list.append(l1)
    
    return users, used_subreddits_list, from_subreddit


def get_subreddits_common_for_both(from_subreddits, used_subreddits, threshold, main_reddits):
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

    TFTR = []
    c = 1
    for subreddit, freq in tf_trump.items():
        if subreddit in tf_biden:
            biden_weight = tf_biden[subreddit]
        else:
            biden_weight = 0

        weight = freq/(biden_weight+c)
        TFTR.append((subreddit, weight))
        TFTR_dict = {n: c for n, c in TFTR}

    return TFTR


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
            if len(common_subreddits) >= n_required_subreddits:
                G.add_edge(users[user_id], users[other_user_id], common_subreddits=(common_subreddits))

    return G


main_reddits = ['President Donald Trump - Trump 2020! - Election Defense Task Force - Stop The Steal!', 
                "President-elect Joe Biden"]

# Load data
users, used_subreddits, from_subreddits = load_data("./data/csv_files/data_partition_2_FriNov13.csv", main_reddits)
#users, used_subreddits2, from_subreddits2 = load_data("./data/csv_files/data_partition_2_FriNov13.csv", main_reddits)

# OPTIONAL: get top n reddits which are too common among both candidates
# Maybe we should say that the lowest 1000 rated reddits, which occurs as a minimum of X in both parties?
subreddits_to_ignore = get_subreddits_common_for_both(from_subreddits, used_subreddits, 0.3, main_reddits)
subreddits_to_ignore = sorted(subreddits_to_ignore, key=lambda x: x[1])

# Create graph
G = create_graph(users, used_subreddits, from_subreddits, n_required_subreddits=1)

# Plot degree dist
plot_degree_dist(G)

# Save graph
#nx.write_gpickle(G, "./data/networks/test.gpickle")

# Load graph
#H = nx.read_gpickle("./data/networks/test.gpickle")



lis = [n for n in G.nodes if G.nodes[n]['from_subreddit'] == main_reddits[1]]
lis = [n for n in G.nodes if G.nodes[n]['from_subreddit'] == main_reddits[0]]

print("")

print("REMEMBER TO CHANGE Joe Biden for President")
