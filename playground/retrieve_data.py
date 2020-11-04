# %%
import praw

with open('./../rcred.json') as json_file:
    creds = json.load(json_file)

reddit = praw.Reddit(client_id=creds['user'],
                     client_secret=creds['secret'], password=creds['password'],
                     user_agent=creds['agent'], username=creds['user'])

subreddit = reddit.subreddit('trump')



# hot_python = subreddit.hot(limit=3)
# for submission in hot_python:
#     if not submission.stickied:
#         print('Title: {}, ups: {}, downs: {}, Have we visited?: {}, subid: {}'.format(submission.title,
#                                                                                                    submission.ups,
#                                                                                                    submission.downs,
#                                                                                                    submission.visited,
#                                                                                                    submission.id))
#         submission.comments.replace_more(limit=0)
#         # limiting to 15 results to save output
#         for comment in submission.comments.list()[:15]:
#             print(20*'#')
#             print('Parent ID:',comment.parent())
#             print('Comment ID:',comment.id)
#             # limiting output for space-saving-sake, feel free to not do this
#             print(comment.body[:200])



# %%
