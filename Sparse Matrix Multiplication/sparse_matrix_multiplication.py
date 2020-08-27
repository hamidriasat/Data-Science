import MapReduce
import sys



mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    L=5 #A matrix rows
    M=5 #A matrix column, #B matrix rows
    N=5 #B matrix column
    # print(record)
    #     for martix a
    if str(record[0]).lower()=="a":
        # print("===")
        for k in range(0,N):
            i=record[1]
            j=record[2]
            tempKey="%s,%s" % (i,k)
            tempValue={}
            tempValue["a(%s,%s)" % (i,j)]=record[3]
            # print(tempKey,tempValue)
            mr.emit_intermediate(tempKey,tempValue)
    else:
        for i in range(0,L):
            j=record[1]
            k=record[2]
            tempKey="%s,%s" % (i,k)
            tempValue={}
            tempValue["b(%s,%s)" % (j,k)]=record[3]
            # print(tempKey,tempValue)
            mr.emit_intermediate(tempKey,tempValue)



def reducer(key, list_of_values):
    print(key,list_of_values)

    tempKey=key.split(",")
    i=int(tempKey[0])
    k=int(tempKey[1])
    total = 0
    a=0
    b=0
    M=5
    for j in range(0,M):
        a=0
        b=0
        for tempVal in list_of_values:
            if "a(%s,%s)" % (i,j) in tempVal:
                a=tempVal["a(%s,%s)" % (i,j)]
                break
        for tempVal in list_of_values:
            if "b(%s,%s)" % (j,k) in tempVal:
                b=tempVal["b(%s,%s)" % (j,k)]
                break

        total+=a*b


    if total!=0:
        print(key,total)
    else:
        print(key)


# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open("matrix.json")
    mr.execute(inputdata, mapper, reducer)
