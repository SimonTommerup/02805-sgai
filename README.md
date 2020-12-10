# Motivation for project


Our motivation for doing this project is to explore two groups of internet users from a network science perspective and bring together a set of tools and techniques we have acquired from the course (02805) Social Graphs and Interactions at the Technical University of Denmarnk (DTU) in a useful way led by our curiosity that will provide real insights. 

Most information in modern days is exchanged on the internet. Political opinions and sentiments are shared at the speed of fiber cables on large internet fora. 

reddit is one of the largest internet fora with over 430 million monthly users from all over the world.  Around 50 million Americans and about a fourth of the Americans in the age between 25 and 29 uses reddit (https://www.oberlo.com/blog/reddit-statistics). 

This means reddit gives a unique insight into what is being discussed in America.

reddit is arranged into so-called subreddits where people discuss various subjects. Two of these subreddits are known as r/DonaldTrump and r/JoeBiden and is about the 2020 Presidential Candidates Donald Trump and Joe Biden and has many thousands of users each. 

We want to explore the similarities and differences in the interests of the users on the two subreddits as well as the similiarities and differences in what they are talking about and in how they are feeling. 


# Data files
Data scraping files can be found in the *project* folder. `data_generator.py` does the actual scraping - and in part `utils.py` where the function `get_data_ids` was built to collect the thread and comment ids. These scripts also utilises the ``reddit.py`` for login credentials and ``merge_data.py`` to unite the different chunks of scraped data. 


# Want to know more?
All content from the project can be found here:
https://asgerfg.wixsite.com/a-polarized-america


