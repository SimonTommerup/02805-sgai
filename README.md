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


### Outline:

Klassificering og community detection:
Node attributes (hvordan klassificere vi users - negative kommentare eller bare parent reddit) - et klassificerings problem
tekstanalyse (sentiment analysis - til klassificering)
netværksanalyse (parent reddit)
frekvens af top-comments på parent reddit 
Community detection/score
Modularity score for trump vs biden partition for each classification
Brug TR term ratio to make word clouds!
“sub-word-clouds” for the most frequent words for the entire network (word clouds for comments der indeholder “covid” fx) 
Partition within each party (“sub-communities”)
Word clouds for each of these using TF-IDF
Network statistics to learn about them?
 
Simple network statistics and analysis:
Network type - random, scale-free etc. (node distribution)
edge properties for most connected nodes (where edge property between two nodes are their common other_subreddits)
top commented subreddits (within each community / overall)
average shortest path within communities (fortæller om diversiteten af vælgerne?)  
average degree within communities (fortæller noget om hvor mange fælles interesser de har)
Most central users with respect to degree centrality (disse users interesser dækker umiddelbart de mest typiske interesser for denne egenskab/subreddit - og dermed måske også trump/biden suportters?)
 
Natural language processing:
Lexical diversity within communities (Er et community mere velformuleret end det andet? - kig eventuelt også på kompleksitet af ord, såsom ordlængde)
Collocations (make america great again?)
Sentiment analysis
Hvilke brugere er typisk mest positive negative (eller hvilken side er mest positiv eller negativ stemt?)
Er der tendenser inden for sub-communities?



# Video script:

### An explanation of the central idea behind your final project 
We want to investigate the "typical" supporter of trump and biden respectively
#### (what is the idea?, 
We will do this looking at social medias. Specifically: reddit. We want to look closer at each candidates' supporters, by 
- investigating which forums (subreddits) their supporters are typically active on
- investigate if anything characterizes their supports' language
The idea is then to create a network where we link users which typically are activate (comments) on the same subreddits apart from trump and biden, and see if there is a tendency. E.g. that trump users typically active on a "election fraud" subreddit compared to biden users.

#### why is it interesting? 
Interesting in many ways: 
- for candidates to understand their supports
- for the world to understand why USA is polarized (if it is?) 
- mere? usikker her :D

#### which datasets did you need to explore the idea?, 
More specifically on the data we are looking at:
- we are looking at two "main" subreddits ("forums") which themes trump and biden respectively
- We then extract the users with most popular comments on these subreddits. 
- For each of these users, we furthermore look into 
    - which other subreddits this user is typically active on
    - how they express themselves on reddit (i.e. their comments!)

#### how did you download them)
We download these by looking at two "main" subreddits: trump_reddit, biden_reddit
- for each of these main reddits, we look at the X most popular threads 
- Then we look at Y users which has posted the most popular comments on each of these X threads 
- This gives us approx. X*Y users for each main subreddit. For each of these we
    - download their comment on the main subreddit
    - download the name of up to 50 other reddits, which they have popular comments on

#### A walk-through of your preliminary data-analysis, addressing (
#### What is the total size of your data? (MB, number of rows, number of variables, etc), What is the network you will be analyzing? (number of nodes? number of links?, degree distributions, what are node attributes?, etc.), What is the text you will be analyzing?, How will you tie the two together?) 

The final network we analyze is then of X nodes and Y links. 
- Each node is a user,
- where links are created if two users {CONDITION}

Each node will be assigned two attributes:
- the main subreddit which the user was extracted from (trump or biden)
- the sentiment score of their comment on the main subreddit

- Edges will be assigned the list which connects the two connected nodes/users

The user comments resulted in Z MB of data. This will also be used to characterize the X supporters language.


#### An outline on the elements you'll need to get to your goal & the implementation plan..
(VÆLGE SÅ MANGE SÅ MULIGT AF.... )

Klassificering og community detection:
Node attributes (hvordan klassificere vi users - negative kommentare eller bare parent reddit) - et klassificerings problem
tekstanalyse (sentiment analysis - til klassificering)
netværksanalyse (parent reddit)
frekvens af top-comments på parent reddit 
Community detection/score
Modularity score for trump vs biden partition for each classification
Brug TR term ratio to make word clouds!
“sub-word-clouds” for the most frequent words for the entire network (word clouds for comments der indeholder “covid” fx) 
Partition within each party (“sub-communities”)
Word clouds for each of these using TF-IDF
Network statistics to learn about them?
 
Simple network statistics and analysis:
Network type - random, scale-free etc. (node distribution)
edge properties for most connected nodes (where edge property between two nodes are their common other_subreddits)
top commented subreddits (within each community / overall)
average shortest path within communities (fortæller om diversiteten af vælgerne?)  
average degree within communities (fortæller noget om hvor mange fælles interesser de har)
Most central users with respect to degree centrality (disse users interesser dækker umiddelbart de mest typiske interesser for denne egenskab/subreddit - og dermed måske også trump/biden suportters?)
 
Natural language processing:
Lexical diversity within communities (Er et community mere velformuleret end det andet? - kig eventuelt også på kompleksitet af ord, såsom ordlængde)
Collocations (make america great again?)
Sentiment analysis
Hvilke brugere er typisk mest positive negative (eller hvilken side er mest positiv eller negativ stemt?)
Er der tendenser inden for sub-communities?






# FRAME TEXTS:
# Scene 0.5 or 1:
Who are the typical Trump and Biden supporters?

# Scene 1, 1.5 or 2:
Do the candidates' supporters have any characerizing interests?
And do one express themselves differently?

# Scene 3
Election campaign material spread accross... ...platforms

# Scene 4
Focusing on reddit

We use PRAW to extract information
- a wrapper to the reddit API 

# Scene 5
Info on supporters are extracted from the candidates' main subreddit pages
(Synes ikke deres egentlige navne er nødvendige. Disse skifter ofte)

# Scene 7+8
Looking at the top 36 threads for each candidate

We extract the top 48 associated comments for each thread

Resulting in 1728 examined users and comments for each candidates' subreddit page. 

# Scene 8.5 (or 9?)
TODO: Måske dette slide skal flyttes til sidst ala: "so why 2600 nodes?"
Filtrated, this gave us XX users for each candidate, which seem sufficient as
1. Users represent only top comments and top threads on r/DonaldTrump and r/JoeBiden.

2. Top comments are the most upvoted over all time.

3. Top comments ensures quality of the nodes, which means
    - The comments are not gibberish.
    - We assume that authors with posts that are upvoted are sincere authors relative to their subreddit.
    - We assume that this reasoning is amplified by only taking top threads.

4. Since top threads and top comments are in a direct sense endorsed by the subreddit, it is assumed that their representativity of the users in a given subreddit is higher compared to comments with few or no upvotes. Therefore we assume that our sample sizes are large enough to represent users on either subreddit.

# Scene 9/10? Asger hjælp
We want a network of users which are connected based on their activity on other subreddits, attempting to capture common interests

# Scene 11
Specifically, we create a bipartite network of two distjoint sets U and S of users and subreddits. A user u is linked to subreddit s, if u has one of its all time top 50 comments on s. (Forestiller mig man kunne lave en firkant eller pile fra U->users og S->electrical fraud, QAnon og Funny cats)

# Scene 12->13 + 14? Asger hjælp
The final network is an undirected network of users, extracted from the bipartite graph. Two users u1 and u2 are connected with weight equal to number of common links to subreddits v in V. I.e. users are only connected if they have commented on the same subreddit. 


# Scene 15:
The final network of users consists of: 

- ZZ nodes of reddit users with two attributes each:
    - from_subreddit (trump or biden)
    - comment (posted on from_subreddit)

- RR edges between users, each with two link attributes:
    - common_subreddits (between the two linked users)
    - weight (length of common_subreddits)

# Scene 16 (lidt hurtigt klip): 
The data consists of MM mb in total. 
( BILLEDE AF PANDAS DATAFRAME PRINT? T Har et!)

# Scene 17 (lidt hurtigt klip):
The final network has degrees (i.e. nr. of users with a common subreddit): 
- Minimum: 1 
- Maximum: 2237
- Average: 1261

(BILLEDE AF DEGREE DIST + WEIGHTED DEGREE DIST. T HAR DEM)

# Scene text analysis:
The comments will form the basis of:

- Sentiment analysis: General statistics on the sentiments across segments of the network.
- Sentiment analysis: Predict communities based on the comment sentiment relative to the subreddit to which it is posted. Are genuine Trump voters more positive on r/DonaldTrump and conversely for Biden voters on r/Biden?
- Natural language processing: WordClouds on the subreddits based on term frequency-term ratio analysis to investigate the themes of each subreddit
- Natural language processing: Investigate the lexical diversity in the communities: Are the Trump communities more eloquent than the Biden communities or vice versa?
- Natural language processing: Investigate the possible collocations in the communities: Slogans, catch-phrases and so on.







#### An outline on the elements you'll need to get to your goal & the implementation plan..
(VÆLGE SÅ MANGE SÅ MULIGT AF.... )

Klassificering og community detection:
Node attributes (hvordan klassificere vi users - negative kommentare eller bare parent reddit) - et klassificerings problem
tekstanalyse (sentiment analysis - til klassificering)
netværksanalyse (parent reddit)
frekvens af top-comments på parent reddit 
Community detection/score
Modularity score for trump vs biden partition for each classification
Brug TR term ratio to make word clouds!
“sub-word-clouds” for the most frequent words for the entire network (word clouds for comments der indeholder “covid” fx) 
Partition within each party (“sub-communities”)
Word clouds for each of these using TF-IDF
Network statistics to learn about them?
 
Simple network statistics and analysis:
Network type - random, scale-free etc. (node distribution)
edge properties for most connected nodes (where edge property between two nodes are their common other_subreddits)
top commented subreddits (within each community / overall)
average shortest path within communities (fortæller om diversiteten af vælgerne?)  
average degree within communities (fortæller noget om hvor mange fælles interesser de har)
Most central users with respect to degree centrality (disse users interesser dækker umiddelbart de mest typiske interesser for denne egenskab/subreddit - og dermed måske også trump/biden suportters?)
 
Natural language processing:
Lexical diversity within communities (Er et community mere velformuleret end det andet? - kig eventuelt også på kompleksitet af ord, såsom ordlængde)
Collocations (make america great again?)
Sentiment analysis
Hvilke brugere er typisk mest positive negative (eller hvilken side er mest positiv eller negativ stemt?)
Er der tendenser inden for sub-communities?