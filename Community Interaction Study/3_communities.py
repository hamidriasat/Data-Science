
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


def separate_user_with_hashtags():
    file_text = open('MetaData/tweets_sentiment.txt', 'r', )

    for line in file_text:
        tweet = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        tweet[0] = (tweet[0]).strip()
        tweet[1] = (tweet[1]).strip()
        if tweet[0] not in user_tweets_sentiment_dict.keys():
            user_tweets_sentiment_dict[tweet[0]] = user_hashtags_celeberties({}, {}, {})

        for index in range(2, len(tweet), 1):
            hashtag_text = tweet[index].strip()

            if hashtag_text not in hashtag_users_dict.keys():
                hashtag_users_dict[hashtag_text] = hashtag_users({}, {}, {})
            hashtag_users_dict[hashtag_text].set_user_list(tweet[0])

            if float(tweet[1]) >= 0.0:
                user_tweets_sentiment_dict[tweet[0]].set_positive_hashtags_list(hashtag_text, tweet[1])
                hashtag_users_dict[hashtag_text].set_positive_hashtags_list(tweet[0], tweet[1])
            elif float(tweet[1]) < 0.0:
                user_tweets_sentiment_dict[tweet[0]].set_negative_hashtags_list(hashtag_text, tweet[1])
                hashtag_users_dict[hashtag_text].set_negative_hashtags_list(tweet[0], tweet[1])

    delete_entries = []
    for keys in hashtag_users_dict.keys():
        if hashtag_users_dict[keys].get_user_list_length() < MINIMUM_HASHTAGS_USER_LENGTH:
            delete_entries.append(keys)

    for key in delete_entries:
        del hashtag_users_dict[key]

    file_text.close()
    print("Users with tweets,sentiment,hashtags are done")
    print("Hashtags with users are done")
def read_user_celeberties():
    file_text = open('MetaData/tweets_followers.txt', 'r')

    for line in file_text:
        user = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        user[0] = (user[0]).strip()
        user[1] = (user[1]).strip()
        if user[1] in user_tweets_sentiment_dict.keys():
            if user[1] not in already_added.keys():
                already_added[user[1]] = True
                user_tweets_sentiment_dict[user[1]].set_celeberties_list(user[0])

                if user[0] not in community_users_hashtags_dict.keys():
                    community_users_hashtags_dict[user[0]] = community_users({}, {})
                if community_users_hashtags_dict[user[0]].get_user_list_length() <= MAXIMUM_COMMUNITY_USER_LENGTH:
                    community_users_hashtags_dict[user[0]].set_user_list(user[1])

    file_text.close()

    delete_entries = []
    for keys in community_users_hashtags_dict.keys():
        if community_users_hashtags_dict[keys].get_user_list_length() < MINIMUM_COMMUNITY_USER_LENGTH:
            delete_entries.append(keys)

    for key in delete_entries:
        del community_users_hashtags_dict[key]

    print("Users with followers are done")
    print("Communities with users are done")
def create_community_hashtags():
    for community_key in community_users_hashtags_dict.keys():
        for user_id in community_users_hashtags_dict[community_key].user_list.keys():

            for hashtag_key in user_tweets_sentiment_dict[user_id].positive_hashtags_list.keys():
                if hashtag_key in hashtag_users_dict:
                    if hashtag_key not in community_users_hashtags_dict[community_key].hashtags_list.keys():
                        community_users_hashtags_dict[community_key].hashtags_list[hashtag_key] = hashtag_users({}, {},
                                                                                                                {})
                    community_users_hashtags_dict[community_key].hashtags_list[hashtag_key].set_positive_hashtags_list(
                        user_id, user_tweets_sentiment_dict[user_id].positive_hashtags_list[hashtag_key])

            for hashtag_key in user_tweets_sentiment_dict[user_id].negative_hashtags_list.keys():
                if hashtag_key in hashtag_users_dict:
                    if hashtag_key not in community_users_hashtags_dict[community_key].hashtags_list.keys():
                        community_users_hashtags_dict[community_key].hashtags_list[hashtag_key] = hashtag_users({}, {},
                                                                                                                {})
                    community_users_hashtags_dict[community_key].hashtags_list[hashtag_key].set_negative_hashtags_list(
                        user_id, user_tweets_sentiment_dict[user_id].negative_hashtags_list[hashtag_key])



    print("Communities with hashtags are done")
def create_interection_point():

    for community_key in community_users_hashtags_dict.keys():
        for hashtag_key in community_users_hashtags_dict[community_key].hashtags_list.keys():
            if hashtag_key not in interection_point_dict.keys():
                temp_list = []
                temp_list.append(community_key)
            else:
                temp_list=interection_point_dict[hashtag_key]
                temp_list.append(community_key)
            interection_point_dict[hashtag_key] = temp_list

    # for key in interection_point_dict.keys():
    #     print("====================================================")
    #     print(key,interection_point_dict[key])
def create_bipartite_graph():

    count=0
    B = nx.Graph()

    # print("Print hashtahs with communitties")
    # for key in interection_point_dict.keys():
    #     print(key,interection_point_dict[key])

    temp_list_hashtags=[]
    temp_list_ids=[]
    temp_list_edges=[]
    edge_color=[]

    for key in interection_point_dict.keys():
        if len(interection_point_dict[key])==2 and count<16:
            count+=1
            temp_list_hashtags.append(key)
            temp_list_ids.extend(interection_point_dict[key])

            for id in interection_point_dict[key]:
                temp_list_edges.append(tuple((key,id )))
                if community_users_hashtags_dict[id].hashtags_list[key].get_hashtag_value()<0.0:
                    edge_color.append("r")
                else:
                    edge_color.append("b")


   
    B.add_edges_from(temp_list_edges)

    # Separate by group
    l, r = nx.bipartite.sets(B)
    pos = {}
    # Update position for node from each group
    pos.update((node, (1, index)) for index, node in enumerate(l),)
    pos.update((node, (2, index)) for index, node in enumerate(r))


    nx.draw(B, with_labels=True,edge_color= edge_color ,pos=pos)
    # dpi shows image size
    plt.savefig('MetaData/bipartite_graph.png',dpi = 400)
    plt.draw()

def detect_conflict_communities():
    conflict_communities_list = []
    for community_keys in community_users_hashtags_dict.keys():
        positive_count=0
        negative_count=0
        for hashtag_key in community_users_hashtags_dict[community_keys].hashtags_list.keys():
            if community_users_hashtags_dict[community_keys].hashtags_list[hashtag_key].get_hashtag_value() >= 0.0:
                positive_count+=1
            else:
                negative_count+=1
        if negative_count!=0:
            if (negative_count/ positive_count)>=.15:
                conflict_communities_list.append(community_keys)

    print("Communities who have 15% of negative sentiment")
    for key in conflict_communities_list:
        print( key)




def writeData():
    # temp1= 'MetaData/user_tweets_sentiment_dict.npy'
    temp2 = 'MetaData/community_users_hashtags_dict' + str(MAXIMUM_COMMUNITY_USER_LENGTH) + '.npy'
    temp3 = 'MetaData/hashtag_users_dict' + str(MINIMUM_HASHTAGS_USER_LENGTH) + '.npy'
    temp4 = 'MetaData/interection_point_dict' + str(MINIMUM_HASHTAGS_USER_LENGTH) + '.npy'

    # np.save(temp1, user_tweets_sentiment_dict)
    np.save(temp2, community_users_hashtags_dict)
    np.save(temp3, hashtag_users_dict)
    np.save(temp4, interection_point_dict)

    print("Data written in files")
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
def remove_users_with_hashtag_length():
    delete_entries = []

    for community_key in community_users_hashtags_dict.keys():
        if len(community_users_hashtags_dict[community_key].hashtags_list) > 250:
            delete_entries.append(community_key)

    for key in delete_entries:
        del community_users_hashtags_dict[key]
def read_user_celeberties_with_previous_state():
    file_text = open('MetaData/tweets_followers.txt', 'r')
    previous = ""

    for line in file_text:
        user = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        user[0] = (user[0]).strip()
        user[1] = (user[1]).strip()
        if previous.__eq__(user[1]):
            user_tweets_sentiment_dict[user[1]].set_celeberties_list(user[0])
        else:
            if user[1] in user_tweets_sentiment_dict.keys():
                user_tweets_sentiment_dict[user[1]].set_celeberties_list(user[0])
                previous = user[1]

    file_text.close()
    print("Users with followers(previous) are done")
    count = 0

    # for community_key in community_users_hashtags_dict.keys():
    #     print(community_users_hashtags_dict[community_key].get_user_list_length(),len(community_users_hashtags_dict[community_key].hashtags_list))
    #     if len(community_users_hashtags_dict[community_key].hashtags_list)<=250:
    #         count+=1
    # print(count)

    # for user_key in user_tweets_sentiment_dict.keys():
    #     print(len(user_tweets_sentiment_dict[user_key].celeberties_list),
    #           len(user_tweets_sentiment_dict[user_key].positive_hashtags_list),
    #           len(user_tweets_sentiment_dict[user_key].negative_hashtags_list))

    # for community_key in community_users_hashtags_dict.keys():
    #     print("==========================")
    #     print(community_key)
    #     for hashtag_key in community_users_hashtags_dict[community_key].hashtags_list.keys():
    #         print(community_users_hashtags_dict[community_key].hashtags_list[hashtag_key].get_hashtag_value())

    for community_key in community_users_hashtags_dict.keys():
        print(community_key, len(community_users_hashtags_dict[community_key].user_list),
              len(community_users_hashtags_dict[community_key].hashtags_list))


if __name__ == '__main__':
    # 1
    # separate_user_with_hashtags()
    # read_user_celeberties()
    # create_community_hashtags()
    # create_interection_point()
    # writeData()

    #2
    readData()
    # create_bipartite_graph()
    detect_conflict_communities()



    print("Done")

    