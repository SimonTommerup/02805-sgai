#%% 
import copy
# illustration of concept

a = {
    "subreddit_id_1" : { 
        "1_thread_1" : ["c1","c2","c3"], 
        "1_thread_2" : ["c1","c2","c3"],
        "1_thread_3" : ["c1","c2","c3"],
        "1_thread_4" : ["c1","c2","c3"], 
        "1_thread_5" : ["c1","c2","c3"],
        "1_thread_6" : ["c1","c2","c3"],
        "1_thread_7" : ["c1","c2","c3"], 
        "1_thread_8" : ["c1","c2","c3"],
        "1_thread_9" : ["c1","c2","c3"],
        },
    "subreddit_id_2" : {  
        "2_thread_1" : ["c1","c2","c3"], 
        "2_thread_2" : ["c1","c2","c3"],
        "2_thread_3" : ["c1","c2","c3"],
        "2_thread_4" : ["c1","c2","c3"], 
        "2_thread_5" : ["c1","c2","c3"],
        "2_thread_6" : ["c1","c2","c3"],
        "2_thread_7" : ["c1","c2","c3"], 
        "2_thread_8" : ["c1","c2","c3"],
        "2_thread_9" : ["c1","c2","c3"],
        },
    }
copy1 = copy.deepcopy(a)
copy2 = copy.deepcopy(a)
copy3 = copy.deepcopy(a)

def split_threads(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


#b = dict(a["subreddit_id_1"].items())


#%%

b = [1,2,3,4,5,6,7,8,9]
print(b)
def split_threads_mod(l, n):
    empty=[]
    for i in range(0, len(l), n):
        empty.append(l[i:i + n])
    return empty

b2 = split_threads_mod(b,3)

print(b2)
#%%

for subreddit_id, thread_ids in copy1.items():
    print(subreddit_id)
    keys = list(a[subreddit_id].keys())
    print("KEYS", keys)
    chunks = split_threads(keys, 3)
    chunk0 = next(iter(chunks))
    for key in keys:
        if key not in chunk0:
            copy1[subreddit_id].pop(key)

for subreddit_id, thread_ids in copy1.items():
    print(thread_ids)




# %%
def _split_threads(l, n):
    splits = []
    for i in range(0, len(l), n):
        splits.append(l[i:i + n])
    return splits

def _package_threads(split_threads):
    s = split_threads
    packages = []
    for k,v in zip(s[0],s[1]):
        k += v
        packages.append(k)
    return packages

def split_data_ids(data_ids, n_splits):
    ids = data_ids
    copies = [copy.deepcopy(ids) for n in range(n_splits)]
    thread_id_lists = []
    for _, thread_ids in ids.items():
        thread_id_lists.append(list(thread_ids.keys()))

    split_thread_ids = [_split_threads(thread_id_list, n_splits) for thread_id_list in thread_id_lists]    
    packaged_thread_ids = _package_threads(split_thread_ids)
    for idx, cpy in enumerate(copies):
        for subreddit_id, _ in ids.items():
            for key in ids[subreddit_id].keys():
                if key not in packaged_thread_ids[idx]:
                    cpy[subreddit_id].pop(key)
    return copies            

b = split_data_ids(a,3)

#%%
print(b)
# %%

for d in b:
    print(d.items())
# %%

test = b[2]
print(test.items())
# %%

threads = 12
comments = 25

no_users = threads*comments
print(no_users)

#%%

a = list(range(1,60))
print(len(a))
print(len(a[47:]))
# %%
... 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60



#%%

