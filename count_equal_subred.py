# %%
import pandas as pd
import numpy as np

columns = ['user', 'from_subreddit', 'comment', 'used_subreddits', 'comment_sentiment']

# %%
df = pd.read_csv("trump.csv")
# %%
df
# %%
used_subreddits = np.array(df.used_subreddits)

not_encoded_list = []



# %%
used_subreddits[0]
# %%
import re

s = 'asdf=5;iwantthis123jasd'
result = re.search("\'(.*)\'", used_subreddits[0])
print(result.group(1))
# %%
all_items = []
for l in used_subreddits:
    all_items += re.findall(r"\'(.*?)\'", l)

# %%
all_items
# %%
import nltk
# %%
fdist = nltk.FreqDist(all_items)
# %%
