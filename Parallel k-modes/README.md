# Parallel k-modes algorithm based on MapReduce

## Implementation of [Paralled K-Mode Clustring](https://ieeexplore.ieee.org/document/7054238)

K-modes is a typical categorical clustering algorithm. I implement K-modes on Hadoop using MapReduce parallel computing model.
#### Data Filtering
Organizing data into a useful form is very important for performing different analysis on data. So it is very important to remove or refill
unrelated data that cannot help us with prediction. For example in our case if object attribute is null then we take modes of object friends 
attributes to refill the null values.
#### Map Phase
Second step is the map phase of mapreduce.it takes two parameters. First is the list of random centroids. Second is record from data set.
Then it computes similarity with each centroid in our case we use Jaccard Similarity you can use any. Then whose similarity is high compared to other centroids is choosen as a key pair of map 
phase and its value is the record.
#### Reducer Phase
Reducer phase receives two inputs key and list of records that are assigned to that key. It take mode of all list of values that was received with that key.
Assign mode to that centroid and update the centroid.


### Code Files
* Data.txt ==>	Input Data
* KModeClustring.py ==> Paper Code
* MapReduceFrameworkForKMODE.py ==> A simple framework for solving map reduce based task on python without installing Hadoop.
* centriods.txt ==> Initial random centriods

Need random centriods as an input you can make as many centriods as you want.

For further details about implementation and input data please check Paper.
```
## Dependies:
Python 2.7
Hadoop 2.6
```
