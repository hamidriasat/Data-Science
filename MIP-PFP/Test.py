import json
# import for getting file name, extension from url
import os
# import for using datatime calss for comparing two times
from datetime import datetime
# for creating dictionary of sets
from collections import defaultdict
# for spark
from pyspark.sql import SQLContext, Row
from pyspark import SparkConf, SparkContext


# file logs data
L= []
# cleaned logs data
Lc=[]
# session list
Sset_list=[]
# page stay time thresh_hold
thresh_hold_1=300
# maximum session time thresh_hold
thresh_hold_2=900


# class representing one log entry
class Log:
    def __init__(self, ip, time, zone, method, url, protocol, status, size):
        self.ip = ip
        self.time = time
        self.zone = zone
        self.method = method
        self.url = url
        self.protocol = protocol
        self.status = status
        self.size = size

    def __str__(self):
        return ('Record ip=%s time=%s zone=%s method=%s url=%s protocol=%s status=%s size=%s'% (str(self.ip), str(self.time), str(self.zone), str(self.method), str(self.url),str(self.protocol), str(self.status),str(self.size)))

# contain list of logs that belong to one session
class Session:
    def __init__(self, ):
        self.session_list = []

    def __str__(self):
        return self.session_list

# contain list of urls that belong to one session
class P:
    def __init__(self, key):
        self.key=key
        self.url_list = []

    def __str__(self):
        return self.url_list

# contain list of ip and urls that belong to one session
class FPip:
    def __init__(self, key):
        self.key=key
        self.ip_list = []
        self.url_list = []

    def __str__(self):
        return ('Record key=%s'% (str(self.key)))



# read data from file and add it to list
def read_file(file_path):
    file_text = open(file_path)
    for line in file_text:
        log_item= line.split(" ")
        # make sure element length is 10
        if len(log_item) == 10:
            L.append(Log(log_item[0], log_item[3], log_item[4]
                            , log_item[5], log_item[6], log_item[7]
                            , log_item[8], log_item[9]))

# step 1
# function for filtering data
# Algorithm 1. Pseudocode for web server log cleaning.
# Input: web server log file: L of n records where L fr1, r2, . . . , rng, where n >>> 1
# 8 3 rihip, time, method, url, protocol, size, status, agent, referreri
# Output: cleaned log file: Lc of m records where Lc fr1, r2, . . . , rmg, where m >>> 1
def filter_data():
    for single_record in L:
        try:
            # check if tuple is not empty
            if single_record!=None:
                # dont include url with these extensions
                filename, file_extension = os.path.splitext(single_record.url)
                if(not(file_extension==".gif" or file_extension==".jpeg" or file_extension==".jpg" or file_extension==".png" or file_extension==".tif" or file_extension==".bmp" or file_extension==".mpeg" or file_extension==".mpg" or file_extension==".xbm" or file_extension==".wav" or file_extension==".mp3" or file_extension==".tif" or file_extension==".mov" or file_extension==".avi" or file_extension==".xml" or file_extension==".iff" or file_extension==".mp4")):
                    # status must be between 200 to 400
                    if int(single_record.status)>=100 and int(single_record.status)< 400:
                        # if all checks are ok then add data to cleaned list
                        Lc.append(single_record)
        except Exception:
            print "========================================"
            print "EXCEPTION1111111111111111111111111111111"
            print (single_record)

# if one ip all logs are found once then dont include them again
already_found={}
# find logs that belong to same users
# then pass those records to session_identification method
# for session creation under thresholds
# code for web user session identification.
def find_similar_logs():
    n=len(Lc)
    for i in range(0,n):
        # if this ip is already searched then dont iterate it again
        if not Lc[i].ip in already_found:
            already_found[Lc[i].ip]=True
            found=False
            # if new ip is found then find next log entries of this ip
            for j in range((i+1), n):
                try:
                    if(Lc[i].ip==Lc[j].ip):
                        # if ip found first time then create new object
                        if not found:
                            # for every new ip create object and add next logs entries to this list
                            Szero_obj = Session()
                            Szero_obj.session_list.append(Lc[i])
                            found=True
                        # add searched log entry into object list
                        Szero_obj.session_list.append(Lc[j])

                except Exception:
                    print "========================================"
                    print "EXCEPTION2222222222222222222222222222222"
                    print Lc[i]
                    print Lc[j]
            if found:
                # when all entries are found then send these log entries object
                # to session_identification method for session identification based on given thresholds
                # to check the founded entries
                # checking_print(Szero_obj)
                session_identification(Szero_obj)

# create different sessions based on log entries under threshold constraints
def session_identification(Szero_obj):
    length=len(Szero_obj.session_list)
    start=0
    end=0
    previous=0
    Sset_obj=Session()
    Sset_obj.session_list.append(Szero_obj.session_list[start])
    added=False
    inElse=False
    for current in range(1,length):
        end=current
        page_time_difference=time_difference(str(Szero_obj.session_list[previous].time[1:]),str(Szero_obj.session_list[current].time[1:]))
        if page_time_difference<= thresh_hold_1:
            session_time_difference = time_difference(str(Szero_obj.session_list[start].time[1:]),
                                                     str(Szero_obj.session_list[end].time[1:]))
            if session_time_difference<=thresh_hold_2:
                Sset_obj.session_list.append(Szero_obj.session_list[current])
                added = True
            else:
                inElse = True
                Sset_list.append(Sset_obj)
                del (Sset_obj)
                Sset_obj = Session()
                Sset_obj.session_list.append(Szero_obj.session_list[current])
                start = current
        else:
            inElse=True
            Sset_list.append(Sset_obj)
            del (Sset_obj)
            Sset_obj = Session()
            Sset_obj.session_list.append(Szero_obj.session_list[current])
            start=current
        previous=current

    if added and not inElse:
        Sset_list.append(Sset_obj)


# P_list contain P type object
# P contain key and list of urls
P_list=[]
# FPip_list contain FPip type object
# P contain key and list of urls and list of ips
FPip_list=[]
# code for generation of sequence data.
# P list contain list of urls in each session
# Fpip_list contain list of ip,url for each session
def sequence_data():
    Sset_list_length=len(Sset_list)
    for i in range(0,Sset_list_length):
        session_length=len(Sset_list[i].session_list)
        P_obj=P(i)
        FPip_obj=FPip(i)
        # because one url will be considered once for one session
        temp_dict={}
        for j in range(0,session_length):
            Sset_obj=Sset_list[i].session_list[j]
            if Sset_obj.url not in temp_dict:
                P_obj.url_list.append(Sset_obj.url)
                temp_dict[Sset_obj.url]=1
            FPip_obj.ip_list.append(Sset_obj.ip)
            FPip_obj.url_list.append(Sset_obj.url)
        P_list.append(P_obj)
        FPip_list.append(FPip_obj)


mips={}
# map and reduce operation is done in this method
def find_mips():
    # create spark contex
    sc = SparkContext(master="local", appName="SecondTry")
    # User specified min. Support threshold for MIPS
    # here it is 20 percent
    minsup_ips = .20 * len(FPip_list)

    # convert founded sessions into rdd
    # for conversion first get data from custom list into new list
    # then convert that list into rdd
    temp_list_for_rdd=[]
    for item in FPip_list:
        length=len(item.url_list)
        for i in range(0,length):
            temp_list_for_rdd.append(Row(ip=item.ip_list[i], url=item.url_list[i]))
    rdd = sc.parallelize(temp_list_for_rdd)

    # for calculating how many times each url occur/accessed in a given data
    # first call map with 1 value for each url in session
    mapping = rdd.map(lambda  x:((x[1],1)))

    # then use groupby to collect all the same urls in one place
    # then filter those url that match the minimum fsp threshold
    # then agin call map to get only url that match the minimum threshold
    total=mapping.groupBy(lambda x:x[0]).filter(lambda x:len(x[1])>minsup_ips).map(lambda x:(x[0]))

    # after that convert frequent found urls into list
    temp_list=total.collect()

    # convert founded urls into dictionary so that searching can be performed easily
    for item in temp_list:
        mips[item]=True

# contain list of frequent sequecnce pattern urls
Fsd_list=[]
# for checking uniqness in founded patterns
found_pattern={}
# this will find frequent sequence patrens from session list by matching it to those
# urls that matched the give threshold minsup_ips
def generate_frequesnt_sequence():
    length = len(P_list)
    for i in range(0, length):
        P_url_list_length = len(P_list[i].url_list)
        # dont include those sessions whose url list is less than 2
        if P_url_list_length > 1:
            P_obj = P(i)
            temp_string=""
            for j in range(0, P_url_list_length):
                if P_list[i].url_list[j] in mips:
                    P_obj.url_list.append(P_list[i].url_list[j])
                    temp_string+=P_list[i].url_list[j]
            # dont include those sessions where frequent sequence pattern url list is less than 2
            # and also dont include those patterns who are already found
            if len(P_obj.url_list) > 1 and not temp_string in found_pattern:
                Fsd_list.append(P_obj)
                found_pattern[temp_string]=True

# show results on console
def show_Fsd():
    for item in Fsd_list:
        print "========================"
        print item.key
        for item_url in item.url_list:
            print item_url

    print "========================"
    print "========================"
    print "========================"
    print "Total mined patterns"
    print len(Fsd_list)


def main(*args):
    read_file(args[0])
    # record length of orignal list
    # print len(L)

    filter_data()
    # record length of filtered list
    # print len(Lc)

    # find logs belong to same user and create user sessions

    find_similar_logs()
    # for checking output of find_similar_logs entries
    # checking_session_identification()

    sequence_data()
    # for checking output
    # checking_sequence_data()
    # checking_sequence_data_2()

    find_mips()

    generate_frequesnt_sequence()

    show_Fsd()



# takes two times and return difference in terms of seconds
def time_difference(time_1,time_2):
    datetime_1 = datetime.strptime(time_1, '%d/%b/%Y:%H:%M:%S')
    datetime_2 = datetime.strptime(time_2, '%d/%b/%Y:%H:%M:%S')
    return (datetime_2-datetime_1).total_seconds()

# print all sessions for testing
def checking_session_identification():
    temp_dictionary = {}
    for item in Sset_list:
        print "====================rrrr"
        if item.session_list[0].ip not in temp_dictionary:
            temp_dictionary[item.session_list[0].ip] = 1
        else:
            number = temp_dictionary[item.session_list[0].ip]
            temp_dictionary[item.session_list[0].ip] = number + 1
        for item_session in item.session_list:
            print item_session

    for number in temp_dictionary:
        if temp_dictionary[number]>1:
            print number
            print temp_dictionary[number]


    print len(Sset_list)

# prints logs of one session object
def checking_print(obj):
    print "==================="
    for temp in obj.session_list:
        print temp

# print all sequence_data for testing
# print their ip and urls
def checking_sequence_data():
    for item in FPip_list:
        length =len(item.ip_list)
        print "================="
        print item.key
        for i in range(0,length):
            print ('Record ip=%s url=%s' % (str(item.ip_list[i]), item.url_list[i]))
# print all sequence_data for testing
# print their urls
def checking_sequence_data_2():
    for item in FPip_list:
        length =len(item.url_list)
        print "================"
        print item.key
        for i in range(0,length):
            print ('url=%s' % (item.url_list[i]))



if __name__ == "__main__":
    # main("webLogData50.txt")
    main("access_log_Jul95")

