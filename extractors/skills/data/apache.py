from ..utils import Skill, MaybeSkill, contextual

__all__ = ["SKILLS"]

ctx = contextual("Apache")

SKILLS: list[Skill] = [
  # HADOOP
  Skill("Apache-Hadoop", ["apache=hadoop", "hadoop"]),

  # VARIOUS
	Skill("Apache-Ambari", ["apache=ambari", "ambari"]), # running app manager
	Skill("Apache-Beam", ["apache=beam"]), # running app manager
	MaybeSkill("Apache-Beam", ["beam"], disambiguate=ctx), # allows you to define data pipelines, but you need to run them on external execution environments (Spark being one such option)
  Skill("Apache-Flume", ["apache=flume", "flume"]), # Hadoop data ingestion (streams, logs) to HDFS
  Skill("Apache-Flink", ["apache=flink", "flink"]), # Stream processing, like Storm but higher-level API, newer tool
  Skill("Apache-Hive", ["apache=hive"]), # Hadoop data warehoose with SQL querying
  MaybeSkill("Apache-Hive", ["hive"], disambiguate=ctx), # /
  Skill("Apache-Kafka", ["apache=kafka", "kafka"]),
  Skill("Apache-Lucene", ["apache=lucene", "lucene"]),
  Skill("Apache-MapReduce", ["apache=mapreduce", "mapreduce"]), # Hadoop data pipilene
  Skill("Apache-Mahout", ["apache=mahout"]), # ML, substituted by Spark
  Skill("Apache-Pig", ["apache=pig"]), # Used to analyze Hadoop data (higher-level MapReduce)
  MaybeSkill("Apache-Pig", ["pig"], disambiguate=ctx), # /
  Skill("Apache-Sqoop", ["apache=sqoop", "sqoop"]), # Hadoop data ingestion from rel. DBs to HDFS
  Skill("Apache-Spark", ["apache=spark", "spark"]), # Replaces MapReduce, much faster (RAM, batched), also ANALYTICS
  Skill("Apache-Storm", ["apache=storm"]), # Like Kafka but for real-time streaming
  MaybeSkill("Apache-Storm", ["storm"], disambiguate=ctx), # /

  # SECURITY
  Skill("Apache-Ranger", ["apache=ranger"]), # used for deciding who can access what resources on a Hadoop cluster with the help of policies
  MaybeSkill("Apache-Ranger", ["ranger"], disambiguate=ctx), # /
  Skill("Apache-Knox", ["apache=knox"]), # decides whether to allow user access to Hadoop cluster or not
  MaybeSkill("Knox", ["knox"], disambiguate=ctx), # /

  # DATABASE
  Skill("Apache-Arrow", ["apache=arrow"]),
  MaybeSkill("Apache-Arrow", ["arrow"], disambiguate=ctx),
  Skill("Apache-Cassandra", ["apache=cassandra", "cassandra"]),
  Skill("Apache-DataFusion", ["apache=datafusion", "datafusion"]), # DataFusion is an extensible SQL query engine that uses Apache Arrow.
  Skill("Apache-HDFS", ["apache=hdfs", "hdfs"]), # Hadoop drive FS
  Skill("Apache-HBase", ["apache=hbase", "hbase"]), # Hadoop NoSQl key-value DB

  # INFRASTRUCTURE
  Skill("Apache-Airflow", ["apache=airflow", "airflow"]), # Airflow is an open-source ETL tool for planning, generating, and tracking processes
  Skill("Apache-Oozie", ["apache=oozie", "oozie"]), # Hadoop jobs workflow scheduler (~ GitHub actions)
]
