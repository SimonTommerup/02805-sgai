import time
import copy
import pickle
import pandas as pd
from reddit import reddit
import utils
from prawcore.exceptions import Forbidden
from prawcore.exceptions import ServerError

def data_generator(data_file_name, data_ids, users_to_skip):
    ids_copy = copy.deepcopy(ids)
    num_subreddits_per_user=50
    sleep_time=30
    data = []
    with open("log.txt", "a") as log:
        try:
            for subreddit_id, thread_ids in ids.items():
                thread_ids_copy = copy.deepcopy(thread_ids)

                subreddit = list(reddit.info(["t5_" + subreddit_id]))[0]

                for thread_id, comment_ids in thread_ids.items():
                    comment_ids_copy = copy.deepcopy(comment_ids)

                    fullnames = ["t1_" + comment_id for comment_id in comment_ids]

                    comments = reddit.info(fullnames=fullnames)
                    for comment in comments:
                        user = reddit.redditor(comment.author.name)
                        used_subreddits = []
                        
                        if comment.author not in users_to_skip:
                            users_to_skip.append(comment.author)

                            try: 
                                for user_comment in user.comments.top(limit=num_subreddits_per_user):
                                    used_subreddit = user_comment.subreddit.title
                                    used_subreddits.append(used_subreddit)

                                comment_ids_copy.remove(comment.id)

                            except Forbidden:
                                t = time.time()
                                log.write("Forbidden: " + time.ctime(t) + "\n")
                                comment_ids_copy.remove(comment.id)
                                continue
                            
                            data_item = [comment.author.name,subreddit.title,comment.body,used_subreddits,None]
                            data.append(data_item)

                    thread_ids_copy[thread_id] = comment_ids_copy
                    
                ids_copy[subreddit_id] = thread_ids_copy

        except ServerError:
            # Log incident
            t = time.time()
            print(f"ServerError Exception. Saving data, then sleeping for {sleep_time} seconds.")
            log.write(f"ServerError: {time.ctime(t)}")

            # Save data
            df = pd.DataFrame(data=data)
            df.to_csv(data_file_name, mode="a", sep=";", header=False, index=False)

            # Sleep and resume
            time.sleep(sleep_time)
            data_generator(data_file_name, ids_copy, users_to_skip)

        df = pd.DataFrame(data=data)
        df.to_csv(data_file_name, mode="a", sep=";", header=False, index=False)

if __name__ == "__main__":
    data_file_name = utils.init_data_file()
    ids = utils.get_data_ids(["donald_trump", "JoeBiden"], num_threads=2, num_comments_per_thread=2)
    users_to_skip =  [None, "AutoModerator"]
    data_generator(data_file_name=data_file_name, data_ids=ids, users_to_skip=users_to_skip)

