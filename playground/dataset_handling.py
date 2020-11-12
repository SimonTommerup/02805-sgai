
# %%
import pandas as pd 
import json
#%%
# With JSON.dumps() 
data = [["a1", "b1", "c1", json.dumps(["1a","2a","3a"]), "d1"]]
columns = ["user","from_subreddit","comment","used_subreddits" ,"comment_sentiment"]
df = pd.DataFrame(data=data, columns=columns)

print(df.columns)

#df.to_csv("data/SAVWTODAT.csv",sep=";",columns=columns,index=False)
#print(df["used_subreddits"][0])
#print(type(df["used_subreddits"][0]))

#%%
# Reload with JSON.loads()
df_reload = pd.read_csv("data_test.csv", sep=";")
print(df_reload["used_subreddits"][0])
print(type(df_reload["used_subreddits"][0]))
print(json.loads(df_reload["used_subreddits"][0]))
print(type(json.loads(df_reload["used_subreddits"][0])))

# %%
#df = pd.read_csv("data_test.csv", sep=";")
columns = ["user","from_subreddit","comment","used_subreddits" ,"comment_sentiment"]
additional_data = [["a2", "b2", "c2", json.dumps(["1b","2b","3b"]), "d2"]]

df = pd.DataFrame(data=additional_data)
df.to_csv("data_test.csv", mode="a", sep=";", header=False, index=False)

#%%
import os
print(os.listdir())




# %%
# Reload with JSON.loads()
df_reload = pd.read_csv("../project/dataset_WedNov111729002020.csv", sep=";")


#%%
print(df_reload["used_subreddits"][0])
print(type(df_reload["used_subreddits"][0]))

#%%
print(json.loads(df_reload["used_subreddits"][0]))
print(type(json.loads(df_reload["used_subreddits"][0])))

# %%
