import json, pprint, requests, textwrap
from pyspark import SparkFiles
host = 'http://localhost:8998'
data = {'kind': 'pyspark'}
headers = {'Content-Type': 'application/json'}
session_url = host + '/sessions/1'
SparkFiles.getRootDirectory()

statements_url = session_url + '/statements'

data = {
  'code': textwrap.dedent("""
    import random
    from pyspark import SparkFiles
    spark_dir = SparkFiles.getRootDirectory()
    print(spark_dir)
    """)
}

r = requests.post(statements_url, data=json.dumps(data), headers=headers)
pprint.pprint(r.json())

statements_url = host + r.headers['location']

r = requests.get(statements_url, headers=headers)


data = {
  'code': textwrap.dedent("""
    from pyspark import SparkFiles
    from os import listdir, path
    spark_dir = SparkFiles.getRootDirectory()
    path_to_txt_file = path.join(spark_dir, 'countme.txt')
    lines = spark.read.text(path_to_txt_file).rdd.map(lambda r:r[0])
    counts = lines.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(add)
    output = counts.collect()
    for (word, count) in output:
        print("%s: %i" % (word, count))
        # log.info("%s: %i" % (word, count))    
    """)
}