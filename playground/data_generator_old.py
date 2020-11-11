#%%
import time
import pandas as pd
from reddit import reddit
from prawcore.exceptions import Forbidden
from prawcore.exceptions import ServerError

num_threads = 20
num_comments_per_thread = 20
num_subreddits_per_user = 50 # Changed from 10
users_to_skip = [None, "AutoModerator"]
file_name = "dataset_10nov.csv"
data = []
log = open("log.txt", "a")
except_count = 1


try: 
    main_subreddits = [reddit.subreddit("donaldtrump"), reddit.subreddit("JoeBiden")]
    main_titles = [s.title for s in main_subreddits]

    for subreddit in main_subreddits:

        subreddit_threads = subreddit.top(limit=num_threads)
        for idx, thread in enumerate(subreddit_threads):
            print(f"Processing {subreddit.title}: Thread {idx} of max {num_threads}")
            thread.comments.replace_more(limit=0)
            comments = thread.comments
            for jdx, comment in enumerate(comments[:num_comments_per_thread]):
                print(f"Processing comment {jdx} of max {num_comments_per_thread}")
                
                if comment.author not in users_to_skip:
                    users_to_skip.append(comment.author)

                    user = reddit.redditor(comment.author.name)
                    used_subreddits = []
                    try:
                        for kdx, user_comment in enumerate(user.comments.top(limit=num_subreddits_per_user)):
                            print(f"Processing used subreddit {kdx} of max {num_subreddits_per_user}")
                            used_subreddit = user_comment.subreddit.title
                            #if not used_subreddit == subreddit.title:
                                #if not used_subreddit in used_subreddits:
                            used_subreddits.append(used_subreddit)

                    except Forbidden:
                        continue
                    
                   # if not len(used_subreddits) < 1:
                    data_item = [comment.author.name,subreddit.title,comment.body,used_subreddits,None]
                    data.append(data_item)

# WE NEED SOME KIND OF WAY TO APPEND
# TO THE EXISTING DATA
except ServerError:
    log.write(f"ServerError exception {except_count}")
    except_count += 1
    time.sleep(60)

log.close()

columns = ["user","from_subreddit","comment","used_subreddits" ,"comment_sentiment"]
df = pd.DataFrame(data=data, columns=columns)
df.to_csv(file_name,sep=";",columns=columns,index=False)



# %%
