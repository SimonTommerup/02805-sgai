import utils
import json
import os
import pandas as pd 

dfp1 = pd.read_csv("../project/data/csv_files/data_partition_1_ThuNov12.csv", sep=";")
dfp2 = pd.read_csv("../project/data/csv_files/data_partition_2_FriNov13.csv", sep=";")
dfp3 = pd.read_csv("../project/data/csv_files/data_partition_3_FriNov13.csv", sep=";")
dfp4 = pd.read_csv("../project/data/csv_files/data_partition_4_SatNov14.csv", sep=";")
dfp5 = pd.read_csv("../project/data/csv_files/data_partition_5_SatNov14.csv", sep=";")
dfp6 = pd.read_csv("../project/data/csv_files/data_partition_6_SunNov15.csv", sep=";")

def simplify_from_reddit(dataframe):
    df = dataframe
    subredditnames = list(set(df["from_subreddit"]))
    for name in subredditnames:
        if "trump" in name.lower():
            df.loc[df["from_subreddit"]==name, "from_subreddit"] = "trump"
        elif "biden" in name.lower():
            df.loc[df["from_subreddit"]==name, "from_subreddit"] = "biden"
    return df, subredditnames

def simplify_from_reddit_in_used_subreddits(dataframe, subredditnames):
    df = dataframe
    for outer_idx, l in enumerate(df["used_subreddits"]):
        l = json.loads(l)
        for inner_idx, element in enumerate(l):
            for name in subredditnames:
                if element == name:
                    if "trump" in name.lower():
                        l[inner_idx] = "trump"
                    elif "biden" in name.lower():
                        l[inner_idx] = "biden"
        l = json.dumps(l)
        df["used_subreddits"][outer_idx] = l
    return df

if __name__ == "__main__":

    # settings
    csv_ext = ".csv"
    csv_file_name = "data_all_merged" + csv_ext
    csv_file_path = os.path.join("data/csv_files", csv_file_name)

    dataframes = [dfp1, dfp2, dfp3, dfp4, dfp5, dfp6]

    df = utils.join_data_partitions(dataframes)
    df = utils.remove_repeated_users(df)
    df, from_reddits = simplify_from_reddit(df)
    df = simplify_from_reddit_in_used_subreddits(df, from_reddits)

    df.to_csv(csv_file_path, sep=";", index=False)




