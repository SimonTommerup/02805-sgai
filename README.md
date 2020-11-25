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



### Outline of "3. Tools, theory and analysis. Describe the process of theory to insight"

- _____________________ Introduction to the analysis _____________________
    What will be analyzed and why?
    "We want to investigate whether the subreddit users can represent each candidate's supporters.. "
    - Present the bipartite network (with plots?)
        - "We build a bipartite network to initially extract a network of users... " 
    - Building a weighted network of users
        - We extract a weighted network of users, as these are the ones we want to characterize. 
        - Present basic NETWORK stats we got from Project A (#Edges, #nodes, avg/min/max degree)
        - Plot the network with (possibly with current classification = from_subreddit)


- _____________________ Extracting networks of interest and classifying users _____________________

    - Extracting the "backbone" of the user network
        - Motive: "As we saw from introduction - weighted is very dense... Might be able to extract to more informative!" 
        - Tools: "Works by applying disperse filters, defined by "...
        - Results: "Resulting network is..." (#Edges, #nodes, avg/min/max degree) + PLOT
        - Discussion: " Will be used as comparison to weighted, to see which one gives more information"

    - Classifying users with community Detection and sentiment analysis
        - Motive: "Classifying users by from_subreddit is not necessarily optimal.
        - Tools: Three compared partitions: from_subreddit, Louvain and sentiment in comment. Modularity. Plots
        - Results: Modularity=... Plots=... #Links_Across_partition=..., MORE to decide the better partition!!?
        - Discussion: From X and Y we find __ as the best partitioning for representing each candidates' supporters
        
    - Detecting communities with the bipartite network? ONLY MAYBE!!
        - Motive: "Bipartite networks might contain additional information, which is discarded in the projection
        - Tools: "Explain how community detection works"...
        - Results: "We saw a lot more!!" or "revealed nothing..."
        - Discussion: "Probably because..."
     
_____________________ Comparing candidate sub-networks (of best partitioning) _____________________

    - Simple Network Statistics for candidate sub-networks
        - Motive: "To compare the two networks in terms of simple statistics"
        - Tools: #Nodes, #Edges, Degrees, densities, median, mode, 
        - Results: "compute them..."
        - Discussion: "This could mean that... "
    
    - Degree Distributions and the Network types
        - Motive: "To understand the characteristics of our networks... Does our network follow power-law? Which could mean..."
        - Tools: explain theory...
        - Results
        - Discussion

    - Advanced statistics (maybe this should be 3 seperate bullets)
        - Motive: "Which supporters are more diverse in interests? which are etc...
        - Tools: Clustering, Shortest paths and centralities in sub-networks?
        - Results
        - Discussion

    - Community detection wihin partitions
        - Motive: "Investigate if any communities within Biden/trump lair"
        - Tools: Louvain
        - Results
        - Dicussion






- _____________________ Comparing text/comments of candidates' supporters _____________________
    - NLP
        - Motive: Is one community more eloquent? Does either community have more catch-phrases? Typical words?
        - Tools: Lexical diversity, collocations, TFTR + wordclouds
        - Results
        - Discussion

    - Sentiment analysis
        - Motive: Is one candidate´s supporters more positive than the other's?
        - Tools: Sentiment analysis of comments
        - Results
        - Discussion









### Outline
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

### Explainer Notebook style guide:

#### Sectioning: 

Headlines: size #
1.,2.,3.,4.,5. 

Subheadlines: size ##
1.1, 2.1, 3.1

Subsubheadlines: size ###
1.1.1, 1.1.2 

Subsubsubheadlines: size ###
1.1.1.1, 1.1.1.2 

#### References: 

Everytime some equation or new tool is used, find the relevant source to reference. 

i.e.  "the Louvain algorithm (Blondel 2008) is used"

Place link or book in References section:

"Fast unfolding of communities in large networks", Blondel et al. (2008), https://arxiv.org/pdf/0803.0476.pdf







