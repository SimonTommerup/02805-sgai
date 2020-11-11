import pandas as pd
import numpy as np
import re
import nltk
import networkx as nx
import matplotlib.pyplot as plt

from tqdm import tqdm


columns = ['user', 'from_subreddit', 'comment', 'used_subreddits', 'comment_sentiment']

# CHOOSE DATA SET HERE
df = pd.read_csv("./data/dataset_20201106.csv", error_bad_lines=False)
used_subreddits = np.array(df.used_subreddits)
users = np.array(df.user)


used_subreddits_list = []
for l in used_subreddits:
    l1 = re.findall(r"\'(.*?)\'[,\]]", l)
    if "Donald Trump - 45th President of the United States of America" in l1:
        l1.remove("Donald Trump - 45th President of the United States of America")
    used_subreddits_list.append(l1)

def get_users_with_common_subreddits(user_id, users, used_subreddits_list):
    users_with_common_subreddits = []
    for other_user_id in range(len(users)):
        if other_user_id != user_id:  # Skip connection to self
            for subr in used_subreddits_list[user_id]:
                if subr in used_subreddits_list[other_user_id]:
                    users_with_common_subreddits.append(users[other_user_id])
                    print(subr)
                    break
    return users_with_common_subreddits

def plot_degree_dist(degrees):
    k_min = np.min(degrees)
    k_max = np.max(degrees)
    print(f"k_min: {min(degrees)}, k_max: {max(degrees)}")
    bin_vector = np.arange(k_min,k_max+2)
    count, bins = np.histogram(degrees, bins=40)
    plt.subplots(figsize=(10,8))  

    # Hist plot
    plt.bar(bins[:len(bins)-1], count, color="darksalmon")
    plt.title("Histogram of the degree distrubution ")   
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.show()
    
## CREATE THE GRAPH
G_tru = nx.Graph()
for i in tqdm(range(len(users))):
    other_users = get_users_with_common_subreddits(i, users, used_subreddits_list)
    for other_user in other_users:
        G_tru.add_edge(users[i], other_user)

    
## PLOT DEGREE DIST
degrees = [val for (node, val) in G_tru.degree()]
plot_degree_dist(degrees)




# Find ud af hvad Simon el. jeg skal sætte over med af parametre
