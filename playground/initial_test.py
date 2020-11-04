#%%
import praw
import json

jcred = open("./../rcred.json")
rcred = json.load(jcred)
jcred.close()

# Reddit instance
r = praw.Reddit(
                client_id=rcred["id"],
                client_secret=rcred["secret"],
                username=rcred["user"],
                password=rcred["pass"],
                user_agent=rcred["agent"]
                )

# Verify authentication
#print(r.user.me())
#print(r.read_only)

# Subreddit instance
s = r.subreddit("trump")

# new threads
s_new = s.top(limit=1)

# the threads object is a generator, 
# so to yield one, we can use iter 
thread = next(iter(s_new))

# remove MoreComments objects from CommentsForest object
# by setting replace_more(limit=0)
thread.comments.replace_more(limit=0)

# print example comment
#print(thread.comments[5].body)

print(thread.comments[5].author)



# Comments object
#c = s.comments
#print(c.parse())


## %%

# %%
