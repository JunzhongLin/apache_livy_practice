FROM john/pyspark:2.3.2-hadoop2.7-py3.7

# ADD Python dependencies
# Please add the external dependent packages here by pip install -r requirements.txt

# Deploy node
COPY start-spark.sh /
CMD ["/bin/bash", "/start-spark.sh"]