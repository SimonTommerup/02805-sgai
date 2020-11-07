# %% Imports
import praw
import pandas as pd
import numpy as np
import json

from prawcore.exceptions import Forbidden


# %% Load crendentials and init reddit object
with open('./../rcred.json') as json_file:
    creds = json.load(json_file)

# Init reddit object
reddit = praw.Reddit(client_id=creds['id'],
                     client_secret=creds['secret'], password=creds['password'],
                     user_agent=creds['agent'], username=creds['user'])



# %% __________________________ Download data __________________________

# TODO: make check so that current subreddit (e.g. trump) is not counted
def get_sub_reddits(user, limit):
    sub_reddits = []
    try:
        for comment in (user.comments.top(limit=limit)):
            if comment.subreddit.title is not subreddit.title:
                
                sub_reddits.append(comment.subreddit.title)
    except Forbidden:
        # Nothing
        print("Excepted")
    return list(set(sub_reddits))




data = []

# Retrieve subreddit and its top threads
subreddit = reddit.subreddit('trump')

n_threads = 10 # number of threads for each subreddit (i.e. trump and biden)
n_comments = 50 # number of comments considered for each of threads
n_other_subreddits = 50

top_threads = subreddit.top(limit=n_threads)

# Loop through comments of each thread
for i, thread in enumerate(top_threads):

    if not thread.stickied:  # TODO: We should consider if we want this

        print('Thread: {}, ups: {}'.format(thread.title, thread.ups))
        thread.comments.replace_more(limit=0)
        
        # Now loop over each comment of current thread
        for j, comment in enumerate(thread.comments.list()[:n_comments]):
            print(f"{(i*n_comments)+j+1}/{n_threads*n_comments}")
            if (comment.author is not None):  # and (comment.author.name not in data): # TODO: if author has more comments, which one do we want?
                
                # Retrieve other subreddits which user has commented TODO: make check if list is empty - if so then continue!
                sub_reddits = get_sub_reddits(comment.author, limit=n_other_subreddits) 
                if len(sub_reddits) > 0:
                    data_item = [comment.author.name, subreddit.title, comment.body, sub_reddits, -1]
                    data.append(data_item)
              




# %% Init data frame
columns = ['user', 'from_subreddit', 'comment', 'used_subreddits', 'comment_sentiment']
df=pd.DataFrame(data,columns=columns)




# %%
