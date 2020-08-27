
import tweepy  
import csv
from tweepy.streaming import json


class user_hashtags_celeberties(object):
    def __init__(self, positive_hashtags_list, positive_hashtags_sentiments, negative_hashtags_list,
                 negative_hashtags_sentiments, neutral_hashtags_list, celeberties_list):
        self.positive_hashtags_list =positive_hashtags_list
        self.positive_hashtags_sentiments=positive_hashtags_sentiments
        self.negative_hashtags_list=negative_hashtags_list
        self.negative_hashtags_sentiments=negative_hashtags_sentiments
        self.neutral_hashtags_list=neutral_hashtags_list
        self.celeberties_list=celeberties_list

    def set_positive_hashtags_list(self, value):
        self.positive_hashtags_list.append(value)

    def set_positive_hashtags_sentiments(self, value):
        self.positive_hashtags_sentiments.append(value)

    def set_negative_hashtags_list(self, value):
        self.negative_hashtags_list.append(value)

    def set_negative_hashtags_sentiments(self, value):
        self.negative_hashtags_sentiments.append(value)

    def set_neutral_hashtags_list(self, value):
        self.neutral_hashtags_list.append(value)

    def set_celeberties_list(self, value):
        self.celeberties_list[value] = True

    def get_positive_hashtags_list(self, value):
        return self.positive_hashtags_list[value]

    def get_positive_hashtags_sentiments(self, value):
        return self.positive_hashtags_sentiments[value]

    def get_negative_hashtags_list(self, value):
        return self.negative_hashtags_list[value]

    def get_negative_hashtags_sentiments(self, value):
        return self.negative_hashtags_sentiments[value]

    def get_neutral_hashtags_list(self, value):
        return self.neutral_hashtags_list[value]

    def get_celeberties_list(self, value):
        if value in self.celeberties_list.keys():
            return True
        else:
            return False


user__tweets_sentiment_dict = {}


def separate_user_with_hashtags():
    file_text = open('MetaData/tweets_sentiment.txt', 'r', )

    for line in file_text:
        tweet = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        tweet[0] = (tweet[0]).strip()
        tweet[1] = (tweet[1]).strip()
        if tweet[0] not in user__tweets_sentiment_dict.keys():
            user__tweets_sentiment_dict[tweet[0]] = user_hashtags_celeberties([],[],[],[],[],{})

        for index in range(2, len(tweet), 1):
            if float(tweet[1]) == 0.0:
                user__tweets_sentiment_dict[tweet[0]].set_neutral_hashtags_list(tweet[index].strip())
            elif float(tweet[1]) > 0.0:
                user__tweets_sentiment_dict[tweet[0]].set_positive_hashtags_list(tweet[index].strip())
                user__tweets_sentiment_dict[tweet[0]].set_positive_hashtags_sentiments(tweet[1])
            elif float(tweet[1]) < 0.0:
                user__tweets_sentiment_dict[tweet[0]].set_negative_hashtags_list(tweet[index].strip())
                user__tweets_sentiment_dict[tweet[0]].set_negative_hashtags_sentiments(tweet[1])

    file_text.close()
    print("Users with tweets,sentiment,hashtags are done")


def read_user_celeberties():
    file_text = open('MetaData/tweets_followers.txt', 'r')

    for line in file_text:
        user = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        user[0] = (user[0]).strip()
        user[1] = (user[1]).strip()
        if user[1] in user__tweets_sentiment_dict.keys():
            user__tweets_sentiment_dict[user[1]].set_celeberties_list(user[0])

    file_text.close()
    print("Users with followers are done")

def read_user_celeberties_with_previous_state():
    file_text = open('MetaData/tweets_followers.txt', 'r')
    previous=""

    for line in file_text:
        user = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        user[0] = (user[0]).strip()
        user[1] = (user[1]).strip()
        if previous.__eq__(user[1]):
            user__tweets_sentiment_dict[user[1]].set_celeberties_list(user[0])
        else:
            if user[1] in user__tweets_sentiment_dict.keys():
                user__tweets_sentiment_dict[user[1]].set_celeberties_list(user[0])
                previous=user[1]


    file_text.close()
    print("Users with followers(previous) are done")

def checking():
    count = 0
    for index in user__tweets_sentiment_dict.keys():
        temp_user = user__tweets_sentiment_dict[index]
        if len(temp_user.positive_hashtags_list) == 233256 and len(temp_user.negative_hashtags_list) == 50982 and len(
                temp_user.neutral_hashtags_list) == 279672:
            count += 1

    print(count)


if __name__ == '__main__':
    #
    # read_user_from_file();
    separate_user_with_hashtags()
    read_user_celeberties()
    # checking()
    # read_user_celeberties_with_previous_state()
    print("sd")
