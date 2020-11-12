#%% 
import copy
# illustration of concept

a = {
    "subreddit_id_1" : { 
        "thread_1" : ["c1","c2","c3"], 
        "thread_2" : ["c1","c2","c3"],
        "thread_3" : ["c1","c2","c3"],
        },
    "subreddit_id_2" : {  
        "thread_1" : ["c1","c2","c3"],
        "thread_2" : ["c1","c2","c3"],
        "thread_3" : ["c1","c2","c3"],
        }
    }

b = copy.deepcopy(a)
print("1: ")
print(b)
print()
for subreddit, thread in a.items():
    for thread, comments in thread.items():
        for comment in comments:
            # do_something()
            # remove comment
            b[subreddit][thread].remove(comment)
    # remove thread
    b[subreddit].pop(thread)
    # remove subreddit
    b.pop(subreddit)

print("2: ")
print(b)
print()

# %%
from prawcore.exceptions import ServerError
class Response:
    status_code=503

raise ServerError(Response)

# %%


import pandas as pd 

df = pd.DataFrame(data=[["1","2","3"],["a","b","c"]], columns=["f","a","t"])
print(df)

df.loc[len(df)] = ["ny","ny","ny"]

print(df)

df2 = pd.DataFrame(columns=["1","2","3"])

print(df2)

# %%

import pandas as pd

#df_nexp = pd.read_csv("data/nexp.csv",sep=";")
df_nexp = pd.read_csv("data/nexp.csv", sep=";")
# %%
#print(df_nexp.columns)

print(df_nexp.columns)
# %%

for k in df_nexp.columns:
    print(df_nexp[k][0])

# %%
