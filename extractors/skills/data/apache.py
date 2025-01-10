from ..utils import Skill, dis_context, dis_neighbours

dis_ctx = dis_context("apache")

SKILLS: list[Skill] = [
  Skill("Apache", ["(@)apache"], "Company"),

  Skill("Apache-Maven", ["apache-maven", "maven"], ""),

  # HADOOP
  Skill("Apache-Hadoop", ["apache-hadoop", "hadoop"], ""),
	Skill("Apache-Ambari", ["apache-ambari", "ambari"], "Running app manager"),
	Skill("Apache-Beam", ["apache-beam"], "Unified model and set of SDKs for defining and executing data processing workflows and data ingestion"),
	Skill("Apache-Beam", ["beam"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Skill("Apache-Flume", ["apache-flume", "flume"], "Hadoop data ingestion (streams, logs) to HDFS"),
  Skill("Apache-Flink", ["apache-flink", "flink"], "Scalable batch and stream data processing"),
  Skill("Apache-Hive", ["apache-hive"], "Data warehouse with SQL querying"),
  Skill("Apache-Hive", ["hive"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Skill("Apache-Kafka", ["apache-kafka", "kafka"], ""),
  Skill("Apache-Lucene", ["apache-lucene", "lucene"], ""),
  Skill("Apache-MapReduce", ["apache-mapreduce", "mapreduce"], "Hadoop data pipilene"),
  Skill("Apache-Mahout", ["apache-mahout"], "ML, substituted by Spark"),
  Skill("Apache-Pig", ["apache-pig"], "Used to analyze Hadoop data (higher-level MapReduce)"),
  Skill("Apache-Pig", ["pig"], disambiguate=[
    dis_neighbours(),
    dis_context("apache", "kafka")
  ]),
  Skill("Apache-Sqoop", ["apache-sqoop", "sqoop"], "Hadoop data ingestion from relational databases to HDFS"),
  Skill("Apache-Spark", ["apache-spark", "spark", "pyspark", "sparksql"], "Distributed data processing engine, a MapReduce replacement"),
  Skill("Apache-Storm", ["apache-storm"], "Like Kafka but for real-time streaming"),
  Skill("Apache-Storm", ["storm"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Skill("Apache-ZooKeeper", ["apache-zookeper"], "Centralized service for process configuration and distributed synchronization"),
  Skill("Apache-ZooKeeper", ["zookeper"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),

  # HADOOP + SECURITY
  Skill("Apache-Ranger", ["apache-ranger"], "Decide who can access what resources on a Hadoop cluster"),
  Skill("Apache-Ranger", ["ranger"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Skill("Apache-Knox", ["apache-knox"], "Decides who can access a Hadoop cluster"),
  Skill("Apache-Knox", ["knox"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),

  # HADOOP + DATABASE
  Skill("Apache-Arrow", ["apache-arrow"], "Columnar memory format optimized for efficient analytics"),
  Skill("Apache-Arrow", ["arrow"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Skill("Apache-Cassandra", ["apache-cassandra", "cassandra"], ""),
  Skill("Apache-DataFusion", ["apache-datafusion", "datafusion"], "Extensible SQL query engine that uses Apache Arrow"),
  Skill("Apache-HDFS", ["apache-hdfs", "hdfs"], "Hadoop drive FS"),
  Skill("Apache-HBase", ["apache-hbase", "hbase"], "Hadoop NoSQl key-value DB"),

  # HADOOP + INFRASTRUCTURE
  Skill("Apache-Airflow", ["apache-airflow", "airflow"], "ETL tool for planning, generating, and tracking processes"),
  Skill("Apache-Oozie", ["apache-oozie", "oozie"], "Hadoop jobs workflow scheduler (~ GitHub actions)"),
  Skill("Apache-ActiveMQ", ["apache-active=mq", "active=mq"], "Message broker"),

  # Apache-Drill
  # Apache-Kylin
]
