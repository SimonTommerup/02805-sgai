#%%
import pandas as pd
import os
import copy
import pickle
import time
from reddit import reddit

#%%
def get_data_ids(title_list, num_threads, num_comments_per_thread):
    subreddits = [reddit.subreddit(title) for title in title_list]
    ids = {}
    for idx, subreddit in enumerate(subreddits):
        print(f"Subreddit {idx+1} of {len(subreddits)}")
        thread_ids = {}
        threads = subreddit.top(limit=num_threads)
        for jdx, thread in enumerate(threads):
            print(f"Thread {jdx+1} of {num_threads}")
            thread.comments.replace_more(limit=0)
            comments = thread.comments
            comment_ids = []
            for comment in comments[:num_comments_per_thread]:
                comment_ids.append(comment.id)
            thread_ids[thread.id] = comment_ids
        ids[subreddit.id] = thread_ids
    return ids

def _split_threads(l, n):
    splits = []
    for i in range(0, len(l), n):
        splits.append(l[i:i + n])
    return splits

def _package_threads(split_threads):
    s = split_threads
    packages = []
    for k,v in zip(s[0],s[1]):
        k += v
        packages.append(k)
    return packages

def split_data_ids(data_ids, num_splits):
    ids = data_ids
    copies = [copy.deepcopy(ids) for n in range(num_splits)]
    thread_id_lists = []
    for _, thread_ids in ids.items():
        thread_id_lists.append(list(thread_ids.keys()))

    split_thread_ids = [_split_threads(thread_id_list, num_splits) for thread_id_list in thread_id_lists]    
    packaged_thread_ids = _package_threads(split_thread_ids)
    for idx, cpy in enumerate(copies):
        for subreddit_id, _ in ids.items():
            for key in ids[subreddit_id].keys():
                if key not in packaged_thread_ids[idx]:
                    cpy[subreddit_id].pop(key)
    return copies

def save_ids_to_pickle(ids, file_name):
    fname = file_name + ".pickle"
    fpath = os.path.join("data/ids_pickles", fname)
    with open(fpath, "wb") as handle:
        pickle.dump(ids, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_ids_from_pickle(partition, main=False):
    fname = "ids_partition_" + str(partition) + ".pickle"
    if main:
        fname = "ids_partition_main" + ".pickle"

    fpath = os.path.join("data/ids_pickles", fname)
    with open(fpath, "rb") as handle:
        ids = pickle.load(handle)
    return ids

def remove_repeated_user_entries(dataframe):
    df = dataframe
    seen_users = []
    data = []
    for idx, user in enumerate(df["user"]):
        if user not in seen_users:
            seen_users.append(user)
            data_item = df.iloc[idx].values.flatten().tolist()
            data.append(data_item)
    cdf = pd.DataFrame(data=data, columns=df.columns)
    return cdf 

def init_data_file(partition):
    partition = str(partition)
    date = local_time()[:8]
    file_name = "data_partition_" + partition + "_" + date + ".csv"
    file_path = os.path.join("data/csv_files", file_name)
    columns = ["user","from_subreddit","comment","used_subreddits" ,"comment_sentiment"]
    df = pd.DataFrame(columns=columns)
    df.to_csv(file_path, sep=";",index=False)
    return file_path

def local_time():
    t = time.ctime()
    t = t.replace(" ", "")
    t = t.replace(":", "")
    return t
#%%
if __name__ == "__main__":
    
    # Settings
    subreddit_titles = ["DonaldTrump", "JoeBiden"]
    num_threads=48
    num_comments_per_thread=48
    num_splits = 6 # 6 threads per subreddit per ids partition

    # Get all ids
    main_ids = get_data_ids(subreddit_titles, num_threads, num_comments_per_thread)

    # Save total ids
    fname = "ids_partition_main"
    save_ids_to_pickle(ids=main_ids, file_name=fname)

    # Split into ids partitions
    split_ids = split_data_ids(main_ids, num_splits)
    """
    for idx, ids in enumerate(split_ids):
        partition_no = str(idx + 1)
        fname = "ids_partition_" + partition_no

        # Save to data/ids_pickles
        save_ids_to_pickle(ids=ids, file_name=fname)
    """

# %%
