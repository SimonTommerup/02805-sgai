# %%
import praw

with open('./../rcred.json') as json_file:
    creds = json.load(json_file)

# Init reddit object
reddit = praw.Reddit(client_id=creds['id'],
                     client_secret=creds['secret'], password=creds['password'],
                     user_agent=creds['agent'], username=creds['user'])

# Retrieve subreddit and its top threads
subreddit = reddit.subreddit('trump')
top_threads = subreddit.top(limit=5)

for thread in top_threads:
    if not thread.stickied: # We should consider if we want this
        print('Title: {}, ups: {}, downs: {}, subid: {}'.format(thread.title,
                                                                thread.ups,
                                                                thread.downs,
                                                                thread.id))
        thread.comments.replace_more(limit=0)
        # limiting to 15 results to save output
        print("Number of comments: ", len(thread.comments.list()[:15]))
        for comment in thread.comments.list()[:15]:
              print(20*'#')
        #     print('Parent ID:',comment.parent())
        #     print('Comment ID:',comment.id)
        #     # limiting output for space-saving-sake, feel free to not do this
              print(comment.body[:10])



# %%
print(2)
print("HEJ")

# %%
print(3)
# %%
