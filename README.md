# apache_livy_practice

## What is Apache Livy:
----
Apache Livy is a service that enables easy interaction with a Spark cluster over a REST interface. It enables easy submission of Spark jobs or snippets of Spark code, synchronous or asynchronous result retrieval, as well as Spark Context management, all via a simple REST interface or an RPC client library. Apache Livy also simplifies the interaction between Spark and application servers, thus enabling the use of Spark for interactive web/mobile applications.

https://livy.apache.org/

## About this repo
----
This repo can be used as a playground for apache livy interacting with Spark. In summary it can be used in two ways:
- use the docker-compose.yml file (in the root folder) to build up an enviroment with spark cluster and livy, the spark application can be submitted by spark standalone mode (client mode for python application).
- use the dockerfile in the test_case folder to build a container with livy and pyspark, through which, the applicaion can be submitted to by spark local mode.

## Project structure
----

```
├── .gitignore
├── LICENSE
├── README.md
├── docker-compose.yml
├── docker_files
│   ├── livy-spark
│   │   ├── Dockerfile
│   │   ├── entrypoint.sh
│   │   └── log4j.properties
│   ├── spark_base
│   │   └── Dockerfile
│   └── spark_dep
│       ├── Dockerfile
│       └── start-spark.sh
├── packages.zip
└── test_case
    ├── Dockerfile
    ├── app
    │   ├── dependencies
    │   │   ├── __init__.py
    │   │   ├── logging_.py
    │   │   └── spark.py
    │   ├── livy_submit
    │   └── wordcount.py
    ├── build_packages.sh
    ├── data
    │   └── countme.txt
    ├── packages.zip
    └── readme.MD
```

## Prerequisites
----
To run this application you need Docker Engine >= 1.10.0. Docker Compose is recommended with a version 1.6.0 or later.

## How to use this repo
----

```bash
git clone https://github.com/JunzhongLin/apache_livy_practice.git
```

### use the single container to run the test case (wordcount)

- build the base spark image
```bash
cd docker_files/spark_base && docker build --tag john/pyspark:2.3.2-hadoop2.7-py3.7 .
```

- build the livy-spark image
```bash
cd ../../test_case && docker build --tag john/livy-spark:0.3.0 .
```

- run the livy-spark container (Note: Please substitute the path/to/current_folder in the following bash command)
```bash
docker run --rm -p8998:8998 -v path/to/current_folder:/job --env LOCAL_DIR_WHITELIST=/job john/livy-spark:0.3.0
```
- submit the test spark job (wordcount)
```bash
curl --request POST \
  --url http://localhost:8998/batches \
  --header 'content-type: application/json' \
  --data '{
	"file": "/job/app/wordcount.py",
	"pyFiles": [
		"/job/app/wordcount.py",
        "/job/packages.zip"
	],
	"files": [
		"/job/data/countme.txt"
	]
}' | python3 -mjson.tool
```

- the build_packages.sh can be used to build the dependecies which can be submitted by --py-files

### use docker-compose

- compose up (please enter the root folder of this repo)
```bash
cd .. && docker compose up -d
```

- submit the spark-application as before.
