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

# Subreddit instance
s = r.subreddit("trump")

# Display attributes
#print(dir(s))

# Comments object
c = s.comments
print(c.parse())


# %%
