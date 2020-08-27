
import nltk
import tweepy  
import csv

from tweepy.streaming import json
import networkx as nx
from networkx.algorithms import bipartite
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity

class community_users(object):
    def __init__(self, user_list, hashtags_list):
        self.user_list = user_list
        self.tweets_text = ""
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



user_tweets_dict = {}
community_users_hashtags_dict = {}


MAXIMUM_COMMUNITY_USER_LENGTH = 50
MINIMUM_COMMUNITY_USER_LENGTH = 10
MINIMUM_HASHTAGS_USER_LENGTH = 50


def read_tweet_text():

    file_text = open('followers_tweets_data.txt', 'r', encoding="utf-8")
    count = 0
    try:
        for line in file_text:
            try:
                count += 1
                tweet = json.loads((line))

                tweet_text = str(tweet["text"])
                tweet_user_id = str(tweet["user"]["id"])
                if len(tweet_text) != 0:
                    if tweet_user_id not in user_tweets_dict.keys():
                        user_tweets_dict[tweet_user_id] = ""
                        user_tweets_dict[tweet_user_id]=user_tweets_dict[tweet_user_id]+tweet_text

               
            except Exception:
                # raise
                print("Internal Exception")

    except Exception as ex:
        print("General Exception")
        # raise

    print("Reading tweets done")

def readData():
    # temp1 = 'MetaData/user_tweets_sentiment_dict.npy'
    temp2 = 'MetaData/community_users_hashtags_dict' + str(MAXIMUM_COMMUNITY_USER_LENGTH) + '.npy'


    global community_users_hashtags_dict


    # user_tweets_sentiment_dict = np.load(temp1, allow_pickle=True).item()
    community_users_hashtags_dict = np.load(temp2, allow_pickle=True).item()

    print("Data read from files")

def combine_community_tweet_text():

    for community_key in community_users_hashtags_dict.keys():
        community_users_hashtags_dict[community_key].hashtags_list=""
        for user_id in community_users_hashtags_dict[community_key].user_list.keys():
            if user_id in user_tweets_dict.keys():
                community_users_hashtags_dict[community_key].hashtags_list=community_users_hashtags_dict[community_key].hashtags_list+user_tweets_dict[user_id]
                del user_tweets_dict[user_id]
    print("Community text combined")

def calculate_cosine_similarity():
    train_list=[]
    for community_key in community_users_hashtags_dict.keys():
        train_list.append(community_users_hashtags_dict[community_key].hashtags_list)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_list)  # finds the tfidf score with normalization

    count=0
    for community_key in community_users_hashtags_dict.keys():
        try:
            print("==============================================")
            print(community_key)
            print( cosine_similarity(tfidf_matrix_train[count],tfidf_matrix_train))  # here the first element of tfidf_matrix_train is matched with other three elements
            count+=1
        except Exception as ex:
            print("General Exception")
            raise

def jaccard_similarity():
    train_list=[]
    for community_key in community_users_hashtags_dict.keys():
        for community_key_inside in community_users_hashtags_dict.keys():
            try:
                print("==============================================")
                print(community_key,community_key_inside)
                # print(community_users_hashtags_dict[community_key].hashtags_list)
                # print( cosine_similarity(community_users_hashtags_dict[community_key].hashtags_list,tfidf_matrix_train))  # here the first element of tfidf_matrix_train is matched with other three elements
                jd_sent_1_2 = nltk.jaccard_distance(set(nltk.ngrams(community_users_hashtags_dict[community_key].hashtags_list, n=3)), set(nltk.ngrams(community_users_hashtags_dict[community_key_inside].hashtags_list, n=3)))
                print(jd_sent_1_2)
            except Exception as ex:
                print("General Exception")
                # raise


if __name__ == '__main__':
    # 1
    # separate_user_with_hashtags()
    # read_user_celeberties()
    # create_community_hashtags()
    # create_interection_point()
    # writeData()

    #2
    readData()
    read_tweet_text()
    combine_community_tweet_text()
    calculate_cosine_similarity()
    # jaccard_similarity()




    print("Done")