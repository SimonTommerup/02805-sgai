import pandas as pd
import time
from reddit import reddit

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

def init_data_file():
    ext = ".csv"
    data_file_name = "dataset_" + local_time() + ext
    columns = ["user","from_subreddit","comment","used_subreddits" ,"comment_sentiment"]
    df = pd.DataFrame(columns=columns)
    df.to_csv(data_file_name, sep=";",index=False)
    return data_file_name

def local_time():
    t = time.ctime()
    t = t.replace(" ", "")
    t = t.replace(":", "")
    return t