import re
import string
from base64 import encode

import tweepy  
import csv
from nltk import TweetTokenizer
from tweepy.streaming import json
from textblob import TextBlob


# unts total number of tweets, tweets of each user
def read_tweets_information_file():
    user_dict = {}
    file_text = open('followers_tweets_data.txt', 'r')
    count = 0
    try:
        for line in file_text:
            count += 1
            tweet = json.loads((line))
        
            if (tweet["user"]["id"] in user_dict.keys()):
                user_dict[tweet["user"]["id"]] += 1
            else:
                user_dict[tweet["user"]["id"]] = 1
    except Exception as ex:
        print("General Exception")

    for keys, value in user_dict.items():
        print(keys, value)

    print("Total Users", len(user_dict))
    print("Total Tweets", count)


def cal_sentiment_analysis():
    file_text = open('followers_tweets_data.txt', 'r')
    count = 0
    try:
        for line in file_text:
            try:
                count += 1
                tweet = json.loads((line))
                print("==========")
                print(tweet["text"])
                tweet_text = str(tweet["text"]).decode("utf-8")
                if len(tweet_text.strip()) != 0:
                    clean_tweet_text = clean_data(tweet_text)
                    # clean_tweet_text=(tweet_text)
                    text_blob = TextBlob(clean_tweet_text)
                    print(clean_tweet_text)
                    print(text_blob.sentiment.polarity)

                    print("==========")
                    if count > 50:
                        break
            except Exception:
                raise
                print("Internal Exception")

    except Exception as ex:
        print("General Exception")
        raise


def clean_data(tweet):
    # Happy Emoticons
    emoticons_happy = ([
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
    ])

    # Sad Emoticons
    emoticons_sad = ([
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
    ])

    # remove stock market tickers like $GE
    tweet = re.sub(r'\$\w*', '', tweet)

    # remove old style retweet text "RT"
    tweet = re.sub(r'^RT[\s]+', '', tweet)

    # remove hyperlinks
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)

    # remove hashtags
    # only removing the hash # sign from the word
    tweet = re.sub(r'#', '', tweet)

    for item in emoticons_happy:
        tweet = str(tweet).replace(item, ' happy ')

    for item in emoticons_sad:
        tweet = str(tweet).replace(item, ' sad ')

    tweet = emoji.demojize(tweet)

    return tweet


# read all hashtags from tweets
def read_hashtags():
    file_text = open('followers_tweets_data.txt', 'r', )
    hashtags_dict = {}
    count = 0
    try:
        for line in file_text:
            try:
                count += 1
                tweet = json.loads((line))
               
                tweet_text = str(tweet["text"].encode("utf-8"))
                if len(tweet_text.strip()) != 0:
                    hashtag_re = re.findall(r'\B#\w*[a-zA-Z]+\w*', tweet_text)
                    # print hashtag_re
                    for item in hashtag_re:
                        item = str(item).replace("#", "")
                        if (item in hashtags_dict.keys()):
                            hashtags_dict[item] += 1
                        else:
                            hashtags_dict[item] = 1

                
            except Exception:
                # raise
                print("Internal Exception")

    except Exception as ex:
        print("General Exception")
        # raise
    for keys, value in hashtags_dict.items():
        if value > 100:
            print(keys, value)

    print("Total hashtags", len(hashtags_dict))
    print("Total Tweets", count)


# save user_id tweet_sentiment list of tweet hashtags into file
def save_tweets_metadata():
    meta_data = open('MetaData/tweets_sentiment.txt', 'a')

    file_text = open('followers_tweets_data.txt', 'r', encoding="utf-8")
    hashtags_dict = {}
    count = 0
    try:
        for line in file_text:
            try:
                count += 1
                tweet = json.loads((line))

                tweet_text = str(tweet["text"])
                tweet_user_id = str(tweet["user"]["id"])
                if len(tweet_text) != 0:

                    text_blob = TextBlob(tweet_text)

                    meta_data.write(tweet_user_id + "\t")
                    meta_data.write("%s" % str(text_blob.sentiment.polarity))
                    # print tweet_text

                    hashtag_re = re.findall(r'\B#\w*[a-zA-Z]+\w*', tweet_text)

                    for item in hashtag_re:
                        item = str(item).replace("#", "")
                        meta_data.write("\t" + (item))
                        if (item in hashtags_dict.keys()):
                            hashtags_dict[item] += 1
                        else:
                            hashtags_dict[item] = 1
                    meta_data.write("\n")

                # print "=========="
                # if count > 500:
                #     break
            except Exception:
                # raise
                print("Internal Exception")

    except Exception as ex:
        print("General Exception")
        # raise

    for keys, value in hashtags_dict.items():
        if value > 100:
            print(keys, value)

    print("Total hashtags", len(hashtags_dict))
    print("Total Tweets", count)


# save all followers whose tweets was scraped into a file
# celeberty_id follower_id
def save_followers_metadata():
    file_text = open('MetaData/tweets_sentiment.txt', 'r', )
    user_dict = {}
    for line in file_text:
        user = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        if user[0] not in user_dict.keys():
            user_dict[user[0]] = True
    file_text.close()

    file_text = open("twitter_rv.net")
    meta_data = open('MetaData/tweets_followers.txt', 'a')

    for line in file_text:
        try:
            user = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
            user[0] = (user[0]).strip()
            user[1] = (user[1]).strip()

            if user[1] in user_dict.keys():
                meta_data.write(user[0] + "\t")
                meta_data.write(user[1] + "\n")
                print("writing", user[1])

        except Exception as ex:
            print("General Exception", user[1])


if __name__ == '__main__':
    #
    # read_tweets_information_file();

    # cal_sentiment_analysis()
    # read_hashtags()
    save_tweets_metadata()
