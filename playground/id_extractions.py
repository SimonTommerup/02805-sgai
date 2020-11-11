#%%
import praw
import json
import itertools

jcred = open("../project/data/rcred.json")
rcred = json.load(jcred)
jcred.close()

# Reddit instance
reddit = praw.Reddit(
                client_id=rcred["id"],
                client_secret=rcred["secret"],
                username=rcred["user"],
                password=rcred["pass"],
                user_agent=rcred["agent"]
                )

#%%
s = reddit.subreddit("donaldtrump")
st, st_backup = itertools.tee(s.top(limit=5))
thread_1 = next(iter(st))
thread_2 = next(iter(st))

print(type(thread_1))

print("Thread ID 1: ", thread_1.id)
print("Thread ID 2: ", thread_2.id)

st = s.top(limit=5)
for thread in st_backup:
    print(thread.id)


print(thread_1._comments_by_id)

# %%
print("Subreddit ID 1: ", thread_1.subreddit_id)
print("Subreddit ID 2: ", thread_2.subreddit_id)
# %%

thread_1.comments.replace_more(limit=0)
print("Thread 1 id: ", thread_1.id)
t_comments = thread_1.comments

submission = reddit.submission(id="jfa96z")
submission.comments.replace_more(limit=0)
s_comments = submission.comments