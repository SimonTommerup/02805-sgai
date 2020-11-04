#%%
import pandas as pd
from reddit import reddit
from prawcore.exceptions import Forbidden

num_threads = 10
num_comments_per_thread = 50
data = []

subreddits = [reddit.subreddit("trump"), reddit.subreddit("JoeBiden")]
for subreddit in subreddits:

    subreddit_threads = subreddit.top(limit=num_threads)
    for thread in subreddit_threads:
        thread.comments.replace_more(limit=0)

        comments = thread.comments
        for comment in comments[:num_comments_per_thread]:

            if comment.author is not None:
                user = reddit.redditor(comment.author.name)
                used_subreddits = []

                try:
                    for user_comment in user.comments.top(limit=100):
                        used_subreddit = user_comment.subreddit
                        if not user_comment.subreddit in used_subreddits:
                            used_subreddits.append(used_subreddit)

                except Forbidden:
                    continue

                data_item = [comment.author.name,subreddit.title,comment.body,used_subreddits,None]
                data.append(data_item)

#%%
# Pandas DataFrame
columns = ["user","from_subreddit","comment","used_subreddits" ,"comment_sentiment"]
df = pd.DataFrame(data=data, columns=columns)

print(len(df))
df

df.to_csv()

# %%
df.to_csv("./../testdata.csv",sep=";",columns=columns,index=False)
# %%


print(df["used_subreddits"][0])
# %%
