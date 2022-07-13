from os import listdir, path
import sys
from operator import add
from dependencies.spark import start_spark
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkFiles
import os

def main():
    spark, log, config = start_spark(
    app_name='word_count',
    local_mode=False,
    # files=[]
    )

    path_to_txt_file = '/job/data/countme.txt'
    lines = spark.read.text(path_to_txt_file)
    lines=lines.rdd.map(lambda r:r[0])
    counts = lines.flatMap(lambda x: x.split(' ')) \
          .map(lambda x: (x, 1)) \
          .reduceByKey(add)
    output = counts.collect()
    for (word, count) in output:
        print("%s: %i" % (word, count))
        # log.info("%s: %i" % (word, count))
    
    spark.stop()

    return None

if __name__ == "__main__":
    main()