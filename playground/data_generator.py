#%%
import pandas as pd
from reddit import reddit
from prawcore.exceptions import Forbidden

num_threads = 1
num_comments_per_thread = 1
users_to_skip = [None, "AutoModerator"]

data = []

main_subreddits = [reddit.subreddit("trump"), reddit.subreddit("JoeBiden")]
main_titles = [s.title for s in main_subreddits]

for subreddit in main_subreddits:

    subreddit_threads = subreddit.top(limit=num_threads)
    for thread in subreddit_threads:
        thread.comments.replace_more(limit=0)

        comments = thread.comments
        for comment in comments[:num_comments_per_thread]:

            if comment.author not in users_to_skip:
                user = reddit.redditor(comment.author.name)
                used_subreddits = []

                try:
                    for user_comment in user.comments.top(limit=10):
                        print("Looping")
                        used_subreddit = user_comment.subreddit.title
                        if not used_subreddit in main_titles:
                            if not used_subreddit in used_subreddits:
                                print("Add")
                                used_subreddits.append(used_subreddit)

                except Forbidden:
                    print("Except")
                    continue

                data_item = [comment.author.name,subreddit.title,comment.body,used_subreddits,None]
                data.append(data_item)

#%%
# Pandas DataFrame
columns = ["user","from_subreddit","comment","used_subreddits" ,"comment_sentiment"]
df = pd.DataFrame(data=data, columns=columns)

print(len(df))
df


# %%
#df.to_csv("./../testdata2.csv",sep=";",columns=columns,index=False)
# %%


print(df["used_subreddits"][0])
# %%
