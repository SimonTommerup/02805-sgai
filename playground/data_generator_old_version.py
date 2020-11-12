import time
import copy
import json
import pickle
import pandas as pd
from reddit import reddit
import utils
from prawcore.exceptions import Forbidden
from prawcore.exceptions import ServerError

def data_generator(data_file_name, ids, users_to_skip):
    ids_copy = copy.deepcopy(ids)
    num_subreddits_per_user=1
    sleep_time=1
    data = []
    ERROR_COUNT = 0
    log_name = "data/log_" + data_file_name.replace(".csv",".txt")
    with open(log_name, "a") as log:
        try:
            for subreddit_id, thread_ids in ids.items():
                subreddit = list(reddit.info(["t5_" + subreddit_id]))[0]
                _cthreads = 1
                _nthreads = len(thread_ids)

                for thread_id, comment_ids in thread_ids.items():
                    print(f"Thread {_cthreads} of {_nthreads}")
                    fullnames = ["t1_" + comment_id for comment_id in comment_ids]
                    comments = reddit.info(fullnames=fullnames)
                    _ccomments = 1
                    _ncomments = len(comment_ids)
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

                            except Forbidden:
                                t = time.time()
                                log.write("Forbidden: " + time.ctime(t) + "\n")
                                _ccomments += 1
                                continue
                            
                            data_item = [comment.author.name,subreddit.title,comment.body,json.dumps(used_subreddits),None]
                            data.append(data_item)

                        ids_copy[subreddit_id][thread_id].remove(comment.id)
                        _ccomments += 1
                    
                    _cthreads +=1
                print(ids_copy)
                ids_copy[subreddit_id].pop(thread_id)
                print(ids_copy)
                ids_copy.pop(subreddit_id)
                print(ids_copy)

        except ServerError:
            # Log incident
            t = time.time()
            print(f"ServerError Exception. Saving data, then sleeping for {sleep_time} seconds.")
            log.write(f"ServerError: {time.ctime(t)} \n")

            # Save data
            df = pd.DataFrame(data=data)
            df.to_csv(data_file_name, mode="a", sep=";", header=False, index=False)

            # Sleep and resume
            #time.sleep(sleep_time)
            #data_generator(data_file_name, ids_copy, users_to_skip)

        df = pd.DataFrame(data=data)
        df.to_csv(data_file_name, mode="a", sep=";", header=False, index=False)
    return ids_copy


if __name__ == "__main__":
    data_file_name = utils.init_data_file()
    print(data_file_name)
    #ids = utils.get_data_ids(["DonaldTrump", "JoeBiden"], num_threads=1, num_comments_per_thread=1)
    #print(ids)
    #users_to_skip =  [None, "AutoModerator"]
    #ids_cpy = data_generator(data_file_name=data_file_name, data_ids=ids, users_to_skip=users_to_skip)
    #print(ids_cpy)

