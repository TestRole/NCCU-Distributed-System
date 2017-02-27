from __future__ import print_function

import re
import sys
from operator import add

from pyspark.sql import SparkSession


def computeContribs(Countrys, rank):
    """Calculates Country contributions to the rank of other Countrys."""
    num_Countrys = len(Countrys)
    for Country in Countrys:
        yield (Country, rank / num_Countrys)
		#print('\n\n\n(Country, rank / num_Countrys) = ' + str((Country, rank / num_Countrys)))

def parseNeighbors(Countrys):
    """Parses a Countrys pair string into Countrys pair."""
    parts = re.split(r'\t', Countrys)
    return parts[7], parts[17]


if len(sys.argv) != 3:
	print("Usage: pagerank <file> <iterations>", file=sys.stderr)
	exit(-1)

spark = SparkSession\
	.builder\
	.appName("PythonPageRank")\
	.getOrCreate()

lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
print('\n\n\n\n\nlines.first() = ' + lines.first())

# Loads all Countrys from input file and initialize their neighbors.
links = lines.map(lambda Countrys: parseNeighbors(Countrys)).filter(lambda x: (x[0] != x[1])).filter(lambda x: (x[0] != '')).filter(lambda x: (x[1] != '')).groupByKey().cache()

# Loads all Countrys with other Country(s) link to from input file and initialize ranks of them to one.
ranks = links.map(lambda Country_neighbors: (Country_neighbors[0], 1.0))
for (link, rank) in ranks.collect():
	print("Initial RANK:  %s has rank: %s." % (link, rank))
	

# Calculates and updates Country ranks continuously using PageRank algorithm.
for iteration in range(int(sys.argv[2])):
	# Calculates Country contributions to the rank of other Countrys.
	contribs = links.join(ranks).flatMap(
		lambda Country_Countrys_rank: computeContribs(Country_Countrys_rank[1][0], Country_Countrys_rank[1][1]))
	print('\n\n\n\n\ncontribs.first()[0] ,  contribs.first()[1] = ' + str(contribs.first()[0]) + ' , ' + str(contribs.first()[1]))
	# Re-calculates Country ranks based on neighbor contributions.
	ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)

# Collects all Country ranks and dump them to console.
f = open('output.csv','a')
for (link, rank) in ranks.sortBy(lambda x:x[1]).collect():
#	print("%s has rank: %s." % (link, rank))
	f.write(str(link) + '\t' + str(rank) + '\n')

spark.stop()
