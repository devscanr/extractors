from ..utils import Skill, contextual, contextual_or_neighbour

__all__ = ["SKILLS"]

ctx = contextual("Apache")
ctxn = contextual_or_neighbour(["Apache"], 2)

SKILLS: list[Skill] = [
  Skill("Apache", ["apache"], ""), # company (etc)

  Skill("Apache-Maven", ["apache-maven", "maven"], ""),

  # HADOOP
  Skill("Apache-Hadoop", ["apache-hadoop", "hadoop"], ""),
	Skill("Apache-Ambari", ["apache-ambari", "ambari"], ""), # running app manager
	Skill("Apache-Beam", ["apache-beam"], ""), # running app manager
	Skill("Apache-Beam", ["beam"], "", disambiguate=ctx), # allows you to define data pipelines, but you need to run them on external execution environments (Spark being one such option)
  Skill("Apache-Flume", ["apache-flume", "flume"], ""), # Hadoop data ingestion (streams, logs) to HDFS
  Skill("Apache-Flink", ["apache-flink", "flink"], "Platform for scalable batch and stream data processing. Like Storm but with higher-level API, a newer tool."),
  Skill("Apache-Hive", ["apache-hive"], ""), # Hadoop data warehoose with SQL querying
  Skill("Apache-Hive", ["hive"], "", disambiguate=ctx), # /
  Skill("Apache-Kafka", ["apache-kafka", "kafka"], ""),
  Skill("Apache-Lucene", ["apache-lucene", "lucene"], ""),
  Skill("Apache-MapReduce", ["apache-mapreduce", "mapreduce"], ""), # Hadoop data pipilene
  Skill("Apache-Mahout", ["apache-mahout"], ""), # ML, substituted by Spark
  Skill("Apache-Pig", ["apache-pig"], ""), # Used to analyze Hadoop data (higher-level MapReduce)
  Skill("Apache-Pig", ["pig"], "", disambiguate=ctx), # /
  Skill("Apache-Sqoop", ["apache-sqoop", "sqoop"], ""), # Hadoop data ingestion from rel. DBs to HDFS
  Skill("Apache-Spark", ["apache-spark", "spark"], "Distributed data processing engine providing a unified API to users for batch and stream processing. A MapReduce replacement."),
  Skill("Apache-Storm", ["apache-storm"], ""), # Like Kafka but for real-time streaming
  Skill("Apache-Storm", ["storm"], "", disambiguate=ctx), # /
  Skill("Apache-ZooKeeper", ["apache-zookeper"], ""), # centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services
  Skill("Apache-ZooKeeper", ["zookeper"], "", disambiguate=ctx), # /

  # HADOOP + SECURITY
  Skill("Apache-Ranger", ["apache-ranger"], ""), # used for deciding who can access what resources on a Hadoop cluster with the help of policies
  Skill("Apache-Ranger", ["ranger"], "", disambiguate=ctx), # /
  Skill("Apache-Knox", ["apache-knox"], ""),     # decides whether to allow user access to Hadoop cluster or not
  Skill("Knox", ["knox"], "", disambiguate=ctx), # /

  # HADOOP + DATABASE
  Skill("Apache-Arrow", ["apache-arrow"], ""), # Lang-independent columnar memory format for flat and hierarchical data, organized for efficient analytics
  Skill("Apache-Arrow", ["arrow"], "", disambiguate=ctx), # /
  Skill("Apache-Cassandra", ["apache-cassandra", "cassandra"], ""),
  Skill("Apache-DataFusion", ["apache-datafusion", "datafusion"], ""), # DataFusion is an extensible SQL query engine that uses Apache Arrow.
  Skill("Apache-HDFS", ["apache-hdfs", "hdfs"], ""), # Hadoop drive FS
  Skill("Apache-HBase", ["apache-hbase", "hbase"], ""), # Hadoop NoSQl key-value DB

  # HADOOP + INFRASTRUCTURE
  Skill("Apache-Airflow", ["apache-airflow", "airflow"], ""), # Airflow is an open-source ETL tool for planning, generating, and tracking processes
  Skill("Apache-Oozie", ["apache-oozie", "oozie"], ""), # Hadoop jobs workflow scheduler (~ GitHub actions)
  Skill("Apache-ActiveMQ", ["apache-active=mq", "active=mq"], ""), # Hadoop jobs workflow scheduler (~ GitHub actions)

  # Apache-Drill
  # Apache-Kylin
]
