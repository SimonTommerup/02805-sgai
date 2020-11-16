import time
import copy
import json
import pickle
import pandas as pd
from reddit import reddit
import utils
from prawcore.exceptions import Forbidden
from prawcore.exceptions import ServerError

class ServerResponse:
    status_code = 503

def data_generator(data_file_name, ids, users_to_skip, exception_flag=False, test=False):
    ids_copy = copy.deepcopy(ids)
    num_subreddits_per_user=50
    sleeptime=60
    log_name = "data/log.txt"
    columns=["user","from_subreddit","comment","used_subreddits" ,"comment_sentiment"]
    df = pd.DataFrame(columns=columns)
    with open(log_name, "a") as log:
        try:
            for subreddit_id, thread_ids in ids.items():
                subreddit = list(reddit.info(["t5_" + subreddit_id]))[0]
                _cthreads = 1
                _nthreads = len(thread_ids)
             
                if subreddit_id == "2t0th" and test:
                    raise ServerError(ServerResponse)
                
                _added_nodes = 0
                for thread_id, comment_ids in thread_ids.items():
                    print(f"Thread {_cthreads} of {_nthreads}")
                    print(f"Added {_added_nodes} nodes")
                    fullnames = ["t1_" + comment_id for comment_id in comment_ids]
                    
                    _ccomments = 1
                    _ncomments = len(comment_ids)

                    comments = reddit.info(fullnames=fullnames)
                    for comment in comments:
                        print(f"Comment {_ccomments} of {_ncomments}")
                        if comment.author not in users_to_skip:
                            users_to_skip.append(comment.author)
                            user = reddit.redditor(comment.author.name)
                            used_subreddits = []
                            try: 
                                for user_comment in user.comments.top(limit=num_subreddits_per_user):
                                    used_subreddit = user_comment.subreddit.title
                                    used_subreddits.append(used_subreddit)
                                    _added_nodes += 1

                            except Forbidden:
                                t = time.time()
                                log.write("Forbidden: " + time.ctime(t) + "\n")
                                _ccomments += 1
                                continue

                            data_item = [comment.author.name,subreddit.title,comment.body,json.dumps(used_subreddits),None]
                            df.loc[len(df)] = data_item

                            ids_copy[subreddit_id][thread_id].remove(comment.id)
                        _ccomments += 1
                    _cthreads += 1

                ids_copy[subreddit_id].pop(thread_id)
                ids_copy.pop(subreddit_id)

                if not exception_flag:
                    df.to_csv(data_file_name,sep=";",columns=columns,index=False)
                
                elif exception_flag:
                    df.to_csv(data_file_name, mode="a",sep=";",columns=columns,index=False)

        except ServerError:
            print(f"ServerError... Sleeping for {sleeptime} seconds.")
            log.write(f"ServerError: {time.ctime()} \n")
            time.sleep(sleeptime)
            data_generator(data_file_name, ids_copy, users_to_skip, exception_flag=True)

if __name__ == "__main__":

    # settings
    tl = ["DonaldTrump"]
    nt = 67
    ncpt = 25
    lti = 59

    # get ids from thread 49-60
    ids = utils.get_data_ids_from_last_thread_idx(title_list=tl, num_threads=nt, num_comments_per_thread=ncpt, last_thread_idx=lti)
    
    # settings for datAa generation
    # load users already in data set
    udf = pd.read_csv("../project/data/csv_files/data_merged_equal_nodes.csv", sep=";")
    users_to_skip = udf["user"].values.tolist()
    users_to_skip.append(None)
    users_to_skip.append("AutoModerator")
    
    data_file_name = "data/csv_files/data_2nd_additional_trump.csv"
    data_generator(data_file_name=data_file_name, ids=ids, users_to_skip=users_to_skip, test=False)
