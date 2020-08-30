
# Identification of Conflict Spreading Nodes in a Community Network

## This repository contain code of Twitter Community Interaction Study.


In social media communities are formed by group of users and communities share views with one another. Understanding how communities fight 
and how to prevent conflicts is important to create better online environment. In this research we studied how communities on Twitter interact with other communities.

### Code Files
1_read_user_tweets.py	==>	code for separating users with hashtags

2_read_followers.py	==>	code for reading user celeberties

3_communities.py	==>	code for creating communities/interection point

4_tfidf_similarity.py	==>	code for creating bipartite graph (to identify which communities are communicating or attacking to other communities. Through bipartite graph we created who-post where network.)

5_pagerank.py		==>	code for pagerank (To check wheather attackers or defenfders have more communication within same group)

For Further details on community interacition study please read the paper "Community Interaction Study.pdf"

For further details on Pseudocode of each file and data please check Proposed Approach and Experiment Section.

### Dependies 
Python 3.7

scikit-learn 0.22.1

NetworkX 2.4
