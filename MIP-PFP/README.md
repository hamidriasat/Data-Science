# Fast prediction of web user browsing behaviours using most interesting patterns

## Implementation of [MIP-PFP](https://journals.sagepub.com/doi/abs/10.1177/0165551516673293?journalCode=jisb)

The browsing behaviors are stored as navigational patterns in web server logs. These weblogs are used to predict frequently accessed patterns of web users, which can be used to predict user behavior and to collect business intelligence. In this project I implemented parallel FP-growth (MIP-PFP) algorithm on the Apache Spark platform for extracting frequent patterns from huge weblogs.

### Code Files

Test.py		==>	Paper Code

webLogData2000.txt	==> Sample input of 2000 points

For further details about implementation and input data please check Paper.
```
Dependies:
Python 2.7
Spark 1.6.3
Hadoop 2.6
```
