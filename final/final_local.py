"""
Example Usage:
bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 1
"""
#DDDDDDDDDIIIIIIIIIMMMMMMMMM
from __future__ import print_function
import re
import sys
from operator import add
from pyspark.sql import SparkSession, SQLContext
from pyspark import SparkContext, SparkConf

path = "gs://dataproc-058afa96-98c4-403a-b7e5-9a4b566f78b7-asia"

def computeContribs(urls, rank):
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    for url in urls:
        yield (url, rank / num_urls)

def parseNeighbors(urls , i ,j):
    """Parses a urls pair string into urls pair."""
    parts = re.split(r'\t', urls)
    return parts[i], parts[j]
	
def dumpThe2Results(rdd , sort=0):
	if (sort):
		rdd = rdd.sortBy(lambda x: x[1])
	for (k, v) in rdd.collect():
		print("%s ; %s." % (k, v))
	
#-------------------------MAIN START
#-------------------------Not Even worth a shit
#if __name__ == "__main__":
'''
if len(sys.argv) < 3:	#!=3 originally
	print("Usage: pagerank <file> <iterations>", file=sys.stderr)
	exit(-1)

print("WARN: This is a naive implementation of PageRank and is given as an example!\n" +
	  "Please refer to PageRank implementation provided by graphx",
	  file=sys.stderr)
'''
# Initialize the spark context.
spark = SparkSession\
	.builder\
	.appName("PythonPageRank")\
	.getOrCreate()

#-------------------------Load CSV
lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])

#-------------------------fetch the column needed by PageRank; PageRankLinks:(country,country)
PageRankLinks = lines.map(lambda urls: parseNeighbors(urls, 7, 17)).\
filter(lambda x: (x[0] != x[1])).\
filter(lambda x: (x[0] != '')).\
filter(lambda x: (x[1] != '')).\
groupByKey().cache()

#-------------------------give the initial values of PageRank by 1; ranks:(country,1.0)
ranks = PageRankLinks.map(lambda url_neighbors: (url_neighbors[0], 1.0))

#-------------------------calculate the values of PageRank iteratively by PageRank algorithm

for iteration in range(int(sys.argv[2])):
	# Calculates URL contributions to the rank of other URLs.
	contribs = PageRankLinks.join(ranks).flatMap(
		lambda url_urls_rank: computeContribs(url_urls_rank[1][0], url_urls_rank[1][1]))
	#print('\n\n\n\n\ncontribs.first()[0] ,  contribs.first()[1] = ' + str(contribs.first()[0]) + ' , ' + str(contribs.first()[1]))
	# Re-calculates URL ranks based on neighbor contributions.
	ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)
	
#-------------------------fetch the column needed by NumMen; PageRankLinks:(country,NumMentions)
NumMen = lines.map(lambda urls: parseNeighbors(urls, 7, 31)).\
filter(lambda x: (x[0] != '')).\
mapValues(lambda x: float(x)).\
cache()

#-------------------------calculate the avg of NumMentions
NMCount = NumMen.map(lambda x: (x[0], 1)).reduceByKey(add)
avgNM = NumMen.reduceByKey(add).join(NMCount).map(lambda x: (x[0], float(x[1][0])/x[1][1]))
TotalNM = NumMen.reduceByKey(lambda x,y: (int(x)+int(y)))

#-------------------------MERGE the page rank and NMCount As (Country, pagerank, NMCount)
Merged = ranks.join(NMCount).map(lambda x: (x[0], x[1][0], x[1][1]))
Merged = Merged.sortBy(lambda x:x[1])

#-------------------------DumpTheResult
for (k, v1, v2) in Merged.collect():
	print("%s\t%s\t%s" % (k, v1, v2))
# dumpThe2Results(ranks,1)
# dumpThe2Results(NMCount,1)

#-------------------------SaveAsFile
#Merged.sortBy(lambda x:x[1]).saveAsTextFile(path + "/MergedOutPut")
#Merged.repartition(1).write.format("csv").save(path + /MergedOutPut")
# ranks.sortBy(lambda x:x[1]).saveAsTextFile("file:///D:/123")	#can use this or like next line
f = open('output.csv','a')
for (k, v1, v2) in Merged.collect():
	f.write(str(k) + ',' + str(v1) + "," + str(v2) + '\n')

spark.stop()

#-------------------------DEMO
'''
lines
	1 2
	1 3
	1 4
	2 1
	3 1
	4 1
INITAIL PageRankLinks
	1	1.0
	3	1.0
	2 	1.0
	4	1.0
contribs.first()[0] ,  contribs.first()[1] = 4 , 0.333333333333
Result
	i = 1
	1 has rank: 2.7.
	3 has rank: 0.433333333333.
	2 has rank: 0.433333333333.
	4 has rank: 0.433333333333.
'''
