# 02805-sgai
Social Graphs and Interactions: Bipartite network exploration on reddit

## Introduction

### Building the network and node properties
Our idea is to take the top (maybe) 100 threads on two opposing subreddits, e.g. Biden and Trump. 
- Then for each thread, we will go over each comment to this thread by a user - these users will be nodes in a set U
- For each of these users, we will save two properties
    1. "trump_reddit" if comment was posted on a trump thread (i.e. on the trump reddit). Otherwise "bidden_reddit".
    2. "trump_supporter" if sentiment ("happyness") of comment is above some threshold. Otherwise "biden_supporter".
- For each user-node u in set U, we will go over other subreddits which they have also commented on and add this subreddit as a new reddit-node v which we gather in a set V. We then make a link from u to v.
- We should then be left with a bipartite network where users are linked to all the subreddits which they have ever commented. 
- Then, we can extract a complete user-network *user_net*, where two users $u_1$ and $u_2$ are linked with link l, if they both are linked to a reddit-node v for any v in V. The link l should have "subreddits" list as property, which contain all the subreddit which links the two users (e.g. if they both commented on 'USA' and 'ANIMALS' subreddits
### Analyze *user_net* network
We can then apply all tools learned in the course to this net.
- If we seperate nodes on either property 1 or 2 above - does their seem to be a community structure? From plots or modularity score? This would mean that e.g. "trump_supporter"s are more likely to be active on another subreddit like "corona virus doesn't exist" or similar...


### TODOs:
- Change encoding of list to json format (by calling json.dump(list))
- Make retrievel script robust to server errors etc. (know where to start script if it stops..)
- Downlaod data!!!