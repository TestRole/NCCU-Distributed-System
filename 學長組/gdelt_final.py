from pyspark.sql import SQLContext
from pyspark.sql import Row
from pyspark import SparkContext
from pyspark.sql import SparkSession


def gdelt(threshold):

	sc =SparkContext()
	sqlContext = SQLContext(sc)

	spark = SparkSession.builder\
		.appName("gdelt_project")\
		.getOrCreate()

	#RawgdeltRDD = sc.textFile("/Users/sf/Documents/Distributed_system/spark-2.0.1-bin-hadoop2.7/data/my/day_data/20161101.export.CSV")
	# RawgdeltRDD = sc.textFile("/Users/sf/Documents/Distributed_system/spark-2.0.1-bin-hadoop2.7/data/my/gdeltEvents-*.csv")
	RawgdeltRDD = sc.textFile("gs://dataproc-8374220d-c2fc-4779-8bfe-8d3461631a17-asia-northeast1/gdelt/gdelt-*.csv")
	#RawgdeltRDD = sc.textFile("gs://gdelt5566/gdeltEvents-*.csv")

	print RawgdeltRDD.count()


	gdeltRDD = RawgdeltRDD.map(lambda line:line.split(","))
	#print gdeltRDD.take(1)
	gdelt_row = gdeltRDD.map(lambda p:
	    Row(
	        Day = (p[1]),
	        Actor1CountryCode = (p[7]),
	        Actor2CountryCode = (p[17]),
	        EventCode = (p[26])
	    )
	)


	gdelt_df = sqlContext.createDataFrame(gdelt_row)
	print gdelt_df.printSchema()

	gdelt = gdelt_df.alias("gdelt")

	# create table and use sql command
	gdelt.createOrReplaceTempView("table")
	# sqlCommand = '''SELECT * FROM table where Actor1CountryCode > '' and Actor2CountryCode > ''
	# 	and Actor1CountryCode!=Actor2CountryCode and
	# 	( Eventcode = '064' or Eventcode = '0214' or Eventcode = '0314' ) limit 50 '''
	sqlCommand = '''SELECT Actor1CountryCode, Actor2CountryCode, count(*) as Count
					FROM table WHERE Actor1CountryCode > '' and Actor2CountryCode > ''
						and Actor1CountryCode!=Actor2CountryCode and
						( Eventcode = '064' or Eventcode = '0214' or Eventcode = '0314' )
					GROUP BY Actor1CountryCode, Actor2CountryCode
					ORDER BY Count DESC'''
	sqlgdelt = spark.sql(sqlCommand)
	# repartition and save dataframe to csv, (send to one worker)
	#sqlgdelt.coalesce(1).write.csv('/Users/sf/Documents/Distributed_system/spark-2.0.1-bin-hadoop2.7/data/my/result.csv')
	print sqlgdelt.show(50)
	# sqlgdelt.rdd.map(lambda r: ";".join([str(c) for c in r])).saveAsTextFile("gs://dataproc-8374220d-c2fc-4779-8bfe-8d3461631a17-asia-northeast1/gdelt-SF")
	sqlgdelt.repartition(1).write.format("csv").save("gs://dataproc-8374220d-c2fc-4779-8bfe-8d3461631a17-asia-northeast1/gdelt-alldata")
	
	
	#print dflist
	resultList = sqlgdelt.rdd.filter(lambda r:int(r.Count)>threshold).map(lambda r: (r.Actor1CountryCode, r.Actor2CountryCode, r.Count)).collect()
	return resultList


def main():
	rl = gdelt(threshold=1)

if __name__ == '__main__':
	main()
	