from os import listdir, path
import sys
from operator import add
from dependencies.spark import start_spark
from pyspark.sql import SparkSession
from pyspark import SparkFiles

def main():
    spark, log, config = start_spark(
    app_name='word_count',
    local_mode=False,
    # files=[]
    )

    # get config file if sent to cluster with --files
    spark_files_dir = SparkFiles.getRootDirectory()
    txt_files = [filename
                for filename in listdir(spark_files_dir)
                if filename.endswith('.txt')]

    # print('spark_files_dir: {}'.format(spark_files_dir))
    # print('where is the py file: '+path.abspath('./wordcoun.py'))
    # for file_name in listdir(spark_files_dir):
    #     print('Found {} inside'.format(file_name))

    if txt_files:
        path_to_txt_file = path.join(spark_files_dir, txt_files[0])
        lines = spark.read.text(path_to_txt_file).rdd.map(lambda r:r[0])
        counts = lines.flatMap(lambda x: x.split(' ')) \
              .map(lambda x: (x, 1)) \
              .reduceByKey(add)
        output = counts.collect()
        for (word, count) in output:
            print("%s: %i" % (word, count))
            # log.info("%s: %i" % (word, count))
    else:
        log.warn('No input txt file found')
    
    spark.stop()

    return None

if __name__ == "__main__":
    main()