"""
This is an example implementation of PageRank. For more conventional use,
Please refer to PageRank implementation provided by graphx

Example Usage:
bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10
"""
from __future__ import print_function

import re
import sys
from operator import add

from pyspark.sql import SparkSession


def computeContribs(urls, rank):
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    for url in urls:
        yield (url, rank / num_urls)
		#print('\n\n\n(url, rank / num_urls) = ' + str((url, rank / num_urls)))

def parseNeighbors(urls):
    """Parses a urls pair string into urls pair."""
    parts = re.split(r'\t', urls)
    return parts[7], parts[17]
    #parts = re.split(r'\s+', urls)
    #return parts[0], parts[1]


#if __name__ == "__main__":
if len(sys.argv) != 3:
	print("Usage: pagerank <file> <iterations>", file=sys.stderr)
	exit(-1)

print("WARN: This is a naive implementation of PageRank and is given as an example!\n" +
	  "Please refer to PageRank implementation provided by graphx",
	  file=sys.stderr)

# Initialize the spark context.
spark = SparkSession\
	.builder\
	.appName("PythonPageRank")\
	.getOrCreate()

lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
print('\n\n\n\n\nlines.first() = ' + lines.first())

# Loads all URLs from input file and initialize their neighbors.
#links = lines.map(lambda urls: parseNeighbors(urls)).distinct().groupByKey().cache()
links = lines.map(lambda urls: parseNeighbors(urls)).filter(lambda x: (x[0] != x[1])).filter(lambda x: (x[0] != '')).filter(lambda x: (x[1] != '')).groupByKey().cache()
#print('\n\n\n\n\nlinks.first()[0] , links.first()[1] = ' + str(links.first()[0]) + ' , ' + str(links.first()[1]))
#for (a, b) in links.collect():
#	print(\n\n\n\n\n\n"Initial LINK:  %s has rank: %s." % (a, str(b)))
#print ('\n\n\n\n\n\n\n\n\n')
#print (links.first()[1][0])

# Loads all URLs with other URL(s) link to from input file and initialize ranks of them to one.
ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))
#print('\n\n\n\n\nranks.first()[0] , ranks.first()[1] = ' + str(ranks.first()[0]) + ' , ' + str(ranks.first()[1]))
for (link, rank) in ranks.collect():
	print("Initial RANK:  %s has rank: %s." % (link, rank))
	

# Calculates and updates URL ranks continuously using PageRank algorithm.
for iteration in range(int(sys.argv[2])):
	# Calculates URL contributions to the rank of other URLs.
	contribs = links.join(ranks).flatMap(
		lambda url_urls_rank: computeContribs(url_urls_rank[1][0], url_urls_rank[1][1]))
	print('\n\n\n\n\ncontribs.first()[0] ,  contribs.first()[1] = ' + str(contribs.first()[0]) + ' , ' + str(contribs.first()[1]))
	# Re-calculates URL ranks based on neighbor contributions.
	ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)

# Collects all URL ranks and dump them to console.
for (link, rank) in ranks.sortBy(lambda x:x[1]).collect():
	print("%s has rank: %s." % (link, rank))

spark.stop()
'''
lines
	1 2
	1 3
	1 4
	2 1
	3 1
	4 1
INITAIL LINKS
	1   1.0
INITAIL LINKS
	1	1.0
	3	1.0
	2 	1.0
	4	1.0
contribs.first()[0] ,  contribs.first()[1] = 4 , 0.333333333333


i = 1
1 has rank: 2.7.
3 has rank: 0.433333333333.
2 has rank: 0.433333333333.
4 has rank: 0.433333333333.
'''
