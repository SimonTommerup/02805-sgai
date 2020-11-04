#%%
import pandas as pd
from reddit import reddit as r

num_threads=1
dataset = pd.read_csv("./../dataset.txt")

subreddits = [r.subreddit("trump")]
for s in subreddits:

    s_top = s.top(limit=num_threads)
    for thread in s_top:
        thread.comments.replace_more(limit=0)

        comments = thread.comments
        for comment in comments[:1]:
            ## check that this works as intended
            dataset["user"] = comment.author
            dataset["comment"] = comment.body
            
            user = reddit.redditor(str(comment.author))
            used_subreddits = []
            for user_comment in user.comments.top(limit=100):
                used_subreddit = user_comment.subreddit
                if not user_comment.subreddit in used_subreddits:
                    used_subreddits.append(used_subreddit)



# %%
