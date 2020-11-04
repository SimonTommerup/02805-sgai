#%%
import pandas as pd
from reddit import reddit as r

num_threads=1
dataset = pd.read_csv("./../dataset.txt")

subreddits = [r.subreddit("trump")]
for s in subreddits:
    # top threads
    s_top = s.top(limit=num_threads)

    # remove MoreComments
    for thread in s_top:
        thread.comments.replace_more(limit=0)

        comments = thread.comments
        for comment in comments[:1]:
            #dataset["user"] = comment.author
            #dataset["comment"] = comment.body
            print(comment.author)
            #print(dir(comment.author))
            print(dir(reddit.redditor(comment.author)))
# %%
