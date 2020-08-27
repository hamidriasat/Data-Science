import MapReduceForKMODE
import sys
import numpy as np
import copy
from collections import Counter
import os

mr = MapReduceForKMODE.MapReduce()

# =============================
# Do not modify above this line
# print(values[8])
# 0=user_id
# 1=public
# 2=completion_percentage
# 3=gender
# 4=region
# 5=last_login
# 6=registration
# 7=AGE
def mapper(data):
    record =data.strip().replace('\'','').split("\t")
    current_record=create_set_from_list(record.copy())

    result={}
    file=open("centriods.txt",encoding='utf-8-sig')
    for value in file:
        centroid=value.split("\t")
        temp_set=set()
        if int(centroid[0])==1:
            temp_set.add("public")
        else:
            temp_set.add("private")

        if int(centroid[1])==1:
            temp_set.add("m")
        else:
            temp_set.add("f")

        temp_set.add(centroid[2].strip().replace('\'',''))

        result[value]=jaccard(temp_set,current_record)

    sorted_by_value = sorted(result.items(), key=lambda kv: kv[1])

    key=sorted_by_value[len(sorted_by_value)-1][0].strip()

    # key="%s,%s,%s,%s" % (record[1],record[3],record[4],record[7])
    # key="%s,%s,%s" % (record[1],record[3],record[4])
    # key="%s,%s" % (record[1],record[3])
    # key="%s,%s,%s,%s,%s" % (record[1],record[3],record[4],record[7],record[50])

    mr.emit_intermediate(key,record)



def reducer(key, list_of_values):
    # file=open("centriods.txt","a",encoding='utf-8-sig')
    # file.write("%s	"% list_of_values[0][1])
    # file.write("%s	"% list_of_values[0][3])
    # file.write("%s"% list_of_values[0][4])
    # file.write("\n")
    # file.close()

    public_list=[]
    gender_list=[]
    region_list=[]
    for value in list_of_values:
        public_list.append(value[1])
        gender_list.append(value[3])
        region_list.append(value[4])

    data = Counter(public_list)
    public_mode=data.most_common(1)[0][0]
    data = Counter(gender_list)
    gender_mode=data.most_common(1)[0][0]
    data = Counter(region_list)
    region_mode=data.most_common(1)[0][0]

    file=open("centriods.txt","a",encoding='utf-8-sig')
    file.write("%s	"% public_mode)
    file.write("%s	"% gender_mode)
    file.write("%s"% region_mode)
    file.write("\n")
    file.close()


def jaccard(a, b):
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def create_set_from_list(record_list):
    if int(record_list[1])==1:
        record_list[1]="public"
    else:
        record_list[1]="private"

    record_list[2]=("%sd") %(str(int(round(np.ceil(int(record_list[2])/5)))))
    if int(record_list[3])==1:
        record_list[3]="m"
    else:
        record_list[3]="f"

    # record_list[5]=record_list[7]
    # return set((record_list[0:6]))

    record_list[6]=record_list[50]
    return set((record_list[0:7]))

    # return set((record_list))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata={}
    inputdata[1]=(("Data.txt"))

    run=True
    count=0
    previous_data=""
    while(run):

        updated_data=open("centriods.txt",encoding='utf-8-sig').read()
        if previous_data==updated_data:
            run=False
        else:
            count+=1
            previous_data=updated_data
            # updated_data.close()
            print(previous_data)
            print("=====================")

            mr.intermediate.clear()
            mr.result.clear()
            mr.execute(inputdata, mapper, reducer)
    # print(len(mr.intermediate))
    print(count)