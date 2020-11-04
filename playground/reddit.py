import praw
import json

jcred = open("./../rcred.json")
rcred = json.load(jcred)
jcred.close()

# Reddit instance
reddit = praw.Reddit(
                client_id=rcred["id"],
                client_secret=rcred["secret"],
                username=rcred["user"],
                password=rcred["pass"],
                user_agent=rcred["agent"]
                )