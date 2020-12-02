
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
import pandas as pd
df_reload = pd.read_csv("../project/data/csv_files/data_partition_1_ThuNov12.csv", sep=";")


#%%
print(df_reload["used_subreddits"][0])
print(type(df_reload["used_subreddits"][0]))

#%%
import json
print(json.loads(df_reload["used_subreddits"][0]))
print(type(json.loads(df_reload["used_subreddits"][0])))

# %%
len(df_reload)
# %%
dfp1 = pd.read_csv("../project/data/csv_files/data_partition_1_ThuNov12.csv", sep=";")
dfp2 = pd.read_csv("../project/data/csv_files/data_partition_2_FriNov13.csv", sep=";")
dfp3 = pd.read_csv("../project/data/csv_files/data_partition_3_FriNov13.csv", sep=";")
dfp4 = pd.read_csv("../project/data/csv_files/data_partition_4_SatNov14.csv", sep=";")

# %%

data1 = [["a1", "b1", "c1", json.dumps(["1a","2a","3a"]), "d1"]]
data2 = [["a2", "b2", "c2", json.dumps(["1b","2b","3b"]), "d2"]]
data3 = [["a3", "b3", "c3", json.dumps(["1c","2c","3c"]), "d3"]]
columns = ["user","from_subreddit","comment","used_subreddits" ,"comment_sentiment"]
df1 = pd.DataFrame(data=data1, columns=columns)
df2 = pd.DataFrame(data=data2, columns=columns)
df3 = pd.DataFrame(data=data3, columns=columns)
df05 = pd.DataFrame(data=data1, columns=columns)
df4 = df1.append(df2)
df4 = df4.append(df3)
df4 = df4.append(df05)

# %%
#print(df4)

print("Iloc", df4["user"].iloc[0])

seen=[]
for idx, user in enumerate(df4["user"]):
    print(idx)
    print(user)
    seen.append(user)

print(seen)

index_ = df4[df4["user"]=="a2"]
print(index_)
#%%


"""
seen2=[]
for idx, user in enumerate(df4["user"]):
    print(idx)
    print(user)
    seen2.append(user)

print(seen2)
"""
# %%

for user in dfp1["user"]:
    if user == "user":
        print("her1")


jdf = dfp1.append(dfp2)
jdf = jdf.append(dfp3)
jdf = jdf.append(dfp4)


idx = dfp1[(dfp1["user"]=="user") & (dfp1["comment"] == "comment")].index
print(len(idx))
#%%

b = [0,1,2,3,4,5]
b0 = [b[0]]
for v in b[1:]:
    print(v)



# %%

def join_data_partitions(dataframes):
    jdf = pd.concat(dataframes, axis=0, join="outer", ignore_index=False)
    return jdf


def remove_repeated_user_entries(dataframe):
    df = dataframe
    seen_users = ["user"]
    data = []
    for idx, user in enumerate(df["user"]):
        if user not in seen_users:
            seen_users.append(user)
            data_item = df.iloc[idx].values.flatten().tolist()
            data.append(data_item)

    cdf = pd.DataFrame(data=data, columns=df.columns)
    return cdf 

# %%
import pandas as pd
dfp1 = pd.read_csv("../project/data/csv_files/data_partition_1_ThuNov12.csv", sep=";")
dfp2 = pd.read_csv("../project/data/csv_files/data_partition_2_FriNov13.csv", sep=";")
dfp3 = pd.read_csv("../project/data/csv_files/data_partition_3_FriNov13.csv", sep=";")
dfp4 = pd.read_csv("../project/data/csv_files/data_partition_4_SatNov14.csv", sep=";")
dfp5 = pd.read_csv("../project/data/csv_files/data_partition_5_SatNov14.csv", sep=";")
dfp6 = pd.read_csv("../project/data/csv_files/data_partition_6_SunNov15.csv", sep=";")


#%%

jdf = join_data_partitions([dfp1, dfp2, dfp3, dfp4,dfp5,dfp6])
indices = jdf[jdf["user"]=="user"].index
print("\"user\" index in joined dataframe: ", indices)
total_users = list(jdf["user"])
print("Total users: ", len(jdf["user"]))
unique_users = list(set(jdf["user"]))
print("User is unique user: ", "user" in unique_users)
print("Unique users: ", len(unique_users))
print("Percentage unique users: ", len(unique_users)/len(total_users)*100)


# %%
jdf_c = remove_repeated_user_entries(jdf)
indices = jdf_c[jdf_c["user"]=="user"].index
print("User index in cleaned dataframe: ", indices)
print("Users after clean: ", len(jdf_c["user"]))
print("Set users after clean: ", len(set(jdf_c["user"])))
print("User is unique user: ", "user" in list(set(jdf_c["user"])))
#%%

df = jdf_c
subredditnames = list(set(jdf_c["from_subreddit"]))
for name in subredditnames:
    if "trump" in name.lower():
        df.loc[df["from_subreddit"]==name, "from_subreddit"] = "trump"
    elif "biden" in name.lower():
        df.loc[df["from_subreddit"]==name, "from_subreddit"] = "biden"

c_subredditnames = list(set(jdf_c["from_subreddit"]))

print(subredditnames)
print(c_subredditnames)


#%%
import json


#%%
before = df["used_subreddits"][0]
print("BEFORE: ", before)
for outer_idx, l in enumerate(df["used_subreddits"]):
    #print("LIST: ", type(l))
    l = json.loads(l)
    #print("LIST: ", type(l))
    for inner_idx, element in enumerate(l):
        for name in subredditnames:
            if element == name:
                if "trump" in name.lower():
                    l[inner_idx] = "trump"
                elif "biden" in name.lower():
                    l[inner_idx] = "biden"
    l = json.dumps(l)
    df["used_subreddits"][outer_idx] = l


after =  df["used_subreddits"][0]

print("AFTER: ", after)
print("SAME STRING: ", before==after)
#%%



#%%
df.to_csv("../project/data/csv_files/data_all_simple_mains.csv", sep=";",index=False)


# %%
import pandas as pd
import json

df = pd.read_csv("../project/data/csv_files/data_all_merged.csv", sep=";")

# %%

print(df.iloc[0]["used_subreddits"])

trump = df[df["from_subreddit"]=="trump"]
biden = df[df["from_subreddit"]=="biden"]

def coa(cand, dataframe):
    c = 0
    for us in dataframe["used_subreddits"]:
        l = json.loads(us)
        if cand in l:
            c += 1
    return c

print(coa("biden", trump))
print(coa("trump", biden))


# %%
nt = len(trump)
nb = len(biden)
print("Trump nodes: ", nt)
print("Biden nodes: ", nb)
print("Total nodes: ", nt + nb)
# %%
