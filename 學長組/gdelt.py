from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import Row

conf = SparkConf().setAppName("helo").setMaster("local")
sc = SparkContext(conf=conf)
#f = sc.textFile("/home/x/Desktop/gdelt/20161025.export.CSV")
#print f.count()




RawgdeltRDD = sc.textFile("/home/x/Desktop/gdelt/")
#print RawgdeltRDD.count()
#print RawgdeltRDD.take(1)
gdeltRDD = RawgdeltRDD.map(lambda line:line.split("\t"))
print gdeltRDD.take(1)
gdelt_row = gdeltRDD.map(lambda p:
    Row(
        Day = (p[1]),
        Actor1CountryCode = (p[7]),
        Actor2CountryCode = (p[17]),
        EventCode = (p[26])
        
        #d = (p[57])
    )
)
#print gdelt_row.take(1)
con = SQLContext(sc)
gdelt_df = con.createDataFrame(gdelt_row)
print gdelt_df.printSchema()
gdelt = gdelt_df.alias("gdelt")
print gdelt.show(100)
