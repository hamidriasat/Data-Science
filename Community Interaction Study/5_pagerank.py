

import tweepy  
import csv

from tweepy.streaming import json
import networkx as nx
from networkx.algorithms import bipartite
import numpy as np
import matplotlib.pyplot as plt




class user_hashtags_celeberties(object):
    def __init__(self, positive_hashtags_list, negative_hashtags_list, celeberties_list):
        self.positive_hashtags_list = positive_hashtags_list
        self.negative_hashtags_list = negative_hashtags_list
        self.celeberties_list = celeberties_list

    def set_positive_hashtags_list(self, key, value):
        if key in self.positive_hashtags_list.keys():
            self.positive_hashtags_list[key] += float(value)
        else:
            self.positive_hashtags_list[key] = float(value)

    def set_negative_hashtags_list(self, key, value):
        if key in self.negative_hashtags_list.keys():
            self.negative_hashtags_list[key] += float(value)
        else:
            self.negative_hashtags_list[key] = float(value)

    def set_celeberties_list(self, value):
        self.celeberties_list[value] = True

    def get_positive_hashtags_list(self, key):
        if key in self.positive_hashtags_list.keys():
            return self.positive_hashtags_list[key]
        else:
            return False

    def get_negative_hashtags_list(self, key):
        if key in self.negative_hashtags_list.keys():
            return self.negative_hashtags_list[key]
        else:
            return False

    def get_celeberties_list(self, value):
        if value in self.celeberties_list.keys():
            return True
        else:
            return False
class community_users(object):
    def __init__(self, user_list, hashtags_list):
        self.user_list = user_list
        self.hashtags_list = hashtags_list

    def set_user_list(self, key):
        self.user_list[key] = True

    def get_user_list(self, value):
        if value in self.user_list.keys():
            return True
        else:
            return False

    def get_user_list_length(self):
        return len(self.user_list)
class hashtag_users(object):
    def __init__(self, positive_hashtags_list, negative_hashtags_list, user_list):
        self.positive_hashtags_list = positive_hashtags_list
        self.negative_hashtags_list = negative_hashtags_list
        self.user_list = user_list


    def set_positive_hashtags_list(self, key, value):
        if key in self.positive_hashtags_list.keys():
            self.positive_hashtags_list[key] += float(value)
        else:
            self.positive_hashtags_list[key] = float(value)

    def set_negative_hashtags_list(self, key, value):
        if key in self.negative_hashtags_list.keys():
            self.negative_hashtags_list[key] += float(value)
        else:
            self.negative_hashtags_list[key] = float(value)


    def set_user_list(self, value):
        self.user_list[value] = True

    def get_positive_hashtags_list(self, key):
        if key in self.positive_hashtags_list.keys():
            return self.positive_hashtags_list[key]
        else:
            return False

    def get_negative_hashtags_list(self, key):
        if key in self.negative_hashtags_list.keys():
            return self.negative_hashtags_list[key]
        else:
            return False

    def get_user_list(self, value):
        if value in self.user_list.keys():
            return True
        else:
            return False

    def get_user_list_length(self):
        return len(self.user_list)

    def get_positive_hashtags_list_mean(self):
        return np.array(list(self.positive_hashtags_list.values())).mean()

    def get_negative_hashtags_list_mean(self):
        return np.array(list(self.negative_hashtags_list.values())).mean()

    def get_hashtag_value(self):
        tempList=[]
        if len(self.positive_hashtags_list)!=0:
            tempList.append(self.get_positive_hashtags_list_mean())
        if len(self.negative_hashtags_list)!=0:
            tempList.append(self.get_negative_hashtags_list_mean())

        return np.array(tempList).mean()



user_tweets_sentiment_dict = {}
community_users_hashtags_dict = {}
hashtag_users_dict = {}
already_added = {}
interection_point_dict = {}
MAXIMUM_COMMUNITY_USER_LENGTH = 50
MINIMUM_COMMUNITY_USER_LENGTH = 10
MINIMUM_HASHTAGS_USER_LENGTH = 50




def readData():
    temp1 = 'MetaData/user_tweets_sentiment_dict.npy'
    temp2 = 'MetaData/community_users_hashtags_dict' + str(MAXIMUM_COMMUNITY_USER_LENGTH) + '.npy'
    temp3 = 'MetaData/hashtag_users_dict' + str(MINIMUM_HASHTAGS_USER_LENGTH) + '.npy'
    temp4 = 'MetaData/interection_point_dict' + str(MINIMUM_HASHTAGS_USER_LENGTH) + '.npy'


    global user_tweets_sentiment_dict
    global community_users_hashtags_dict
    global hashtag_users_dict
    global interection_point_dict

    user_tweets_sentiment_dict = np.load(temp1, allow_pickle=True).item()
    community_users_hashtags_dict = np.load(temp2, allow_pickle=True).item()
    hashtag_users_dict = np.load(temp3, allow_pickle=True).item()
    interection_point_dict = np.load(temp4, allow_pickle=True).item()

    print("Data read from files")

def create_graph():
    first_community_key="53"
    second_community_key="57"
    
    G = nx.Graph()
    first_set_nodes=set()
    second_set_nodes=set()
    my_teleport_set={}
    for user_id_first in community_users_hashtags_dict[first_community_key].user_list.keys():
        G.add_node(user_id_first)
        first_set_nodes.add(user_id_first)
        my_teleport_set[user_id_first] = 1
    for user_id_second in community_users_hashtags_dict[second_community_key].user_list.keys():
        G.add_node(user_id_second)
        second_set_nodes.add(user_id_second)
        my_teleport_set[user_id_second]= 0

    for hashtag_key in hashtag_users_dict.keys():
        if hashtag_key in community_users_hashtags_dict[first_community_key].hashtags_list.keys() and hashtag_key in community_users_hashtags_dict[second_community_key].hashtags_list.keys():

            temp_list_1=[]
            temp_list_2=[]
            for user_id in hashtag_users_dict[hashtag_key].user_list.keys():
                if user_id in community_users_hashtags_dict[first_community_key].user_list.keys():
                    temp_list_1.append(user_id)
                if user_id in community_users_hashtags_dict[second_community_key].user_list.keys():
                    temp_list_2.append(user_id)
            for item in temp_list_1:
                for item2 in temp_list_2:
                    G.add_edge(item,item2)



    print(len(G.nodes))
    delete_list=[]
    for node in G.nodes():
        if G.degree(node) < 1:
            delete_list.append(node)
    for node in delete_list:
        G.remove_node(node)
        first_set_nodes.discard(node)
        second_set_nodes.discard(node)
        del my_teleport_set[node]

    print(len(G.nodes))
    print(len(my_teleport_set))


    

    pr = nx.pagerank(G,personalization=my_teleport_set)

    attacker = []
    defender = []
    for key in my_teleport_set.keys():
        if my_teleport_set[key] ==1:
            attacker.append(pr[key])
        else:
            defender.append(pr[key])

    print(np.array(attacker).mean())
    print(np.array(defender).mean())




if __name__ == '__main__':


    readData()
    create_graph()


    print("Done")

