from ..utils import Skill, contextual, contextual_or_neighbour

__all__ = ["SKILLS"]

ctx = contextual("Amazon")
ctxn = contextual_or_neighbour(["Amazon"], 2)

SKILLS: list[Skill] = [
  Skill("Amazon", ["amazon"], ""), # company (etc)

  # AWS
  Skill("Amazon-WS", ["amazon=web=services", "aws"], ""),
  Skill("Amazon-Athena", ["(amazon=)aws=athena", "amazon=athena"], ""), # analytics, ML + SQL over S3
  Skill("Amazon-Athena", ["athena"], "", disambiguate=ctx),             # /
  Skill("Amazon-Aurora", ["(amazon=)aws=aurora", "amazon=aurora"], ""), # managed DB
  Skill("Amazon-Aurora", ["aurora"], "", disambiguate=ctx),             # /
  Skill("Amazon-Beanstalk", ["(amazon=)aws=beanstalk", "amazon=beanstalk", "beanstalk"], ""), # webapp deployment
  Skill("Amazon-CloudFront", ["(amazon=)aws=cloudfront", "amazon=cloudfront", "cloudfront"], ""), # CDN
  Skill("Amazon-CloudWatch", ["(amazon=)aws=cloudwatch", "amazon=cloudwatch", "cloudwatch"], ""), # monitoring umbrella
  Skill("Amazon-DynamoDB", ["(amazon=)aws=dynamo=db", "amazon=dynamo=db", "dynamo=db"], ""), # distributed NoSQL DB
  Skill("Amazon-EC2", ["(amazon=)aws=ec2", "amazon=ec2", "ec2"], ""), # elastic compute cloud
  Skill("Amazon-ECS", ["(amazon=)aws=ecs", "amazon=ecs", "ecs"], ""), # elastic container services
  Skill("Amazon-EBS", ["(amazon=)aws=ebs", "amazon=ebs", "ebs"], ""), # elastic block store
  Skill("Amazon-ElastiCache", ["(amazon=)aws=elasticache", "amazon=elasticache", "elasticache"], ""), # caching
  Skill("Amazon-Glue", ["(amazon=)aws=glue", "amazon=glue"], ""), # batch data ingestion, data pipeline orchestration
  Skill("Amazon-Glue", ["glue"], "", disambiguate=ctx),           # /
  Skill("Amazon-IAM", ["(amazon=)aws=iam", "amazon=iam"], ""), # identity and access management
  Skill("Amazon-IAM", ["iam"], "", disambiguate=ctx),          # /
  Skill("Amazon-Lambda", ["(amazon=)aws=lambda", "amazon=lambda"], ""), # lambda
  Skill("Amazon-Lambda", ["lambda"], "", disambiguate=ctx),             # /
  Skill("Amazon-Kinesis", ["(amazon=)aws=kinesis", "amazon=kinesis", "kinesis"], ""), # streaming data ingestion & analytics
  Skill("Amazon-Neptune", ["(amazon=)aws=neptune", "amazon=neptune", "neptune"], ""), # graph db
  Skill("Amazon-SNS", ["(amazon=)aws=sns", "amazon=sns", "sns"], ""), # simple notification service
  Skill("Amazon-SQS", ["(amazon=)aws=sqs", "amazon=sqs", "sqs"], ""), # simple queue service
  Skill("Amazon-S3", ["(amazon=)aws=s3", "amazon=s3", "s3"], ""),     # object storage
  Skill("Amazon-RDS", ["(amazon=)aws=rds", "amazon=rds", "rds"], ""), # relational database service
  Skill("Amazon-Redshift", ["(amazon=)aws=redshift", "amazon=redshift", "redshift"], ""), # data warehouse & BI
  Skill("Amazon-SageMaker", ["(amazon=)aws=sagemaker", "amazon=sagemaker", "sagemaker"], ""), # deploy ML
  Skill("Amazon-VPC", ["(amazon=)aws=vpc", "amazon=vpc"], ""), # virtual private cloud
  Skill("Amazon-VPC", ["vpc"], "", disambiguate=ctx),          # /

  # SUSPENDED (for now)
  # Autoscale
  # API Gateway
  # App Load Balancer
  # CloudTrail
  # EMR
  # EventBridge
  # QuickSight -- data analytics, dashboards
  # Rekognition
  # Route 53
  # SageMaker
  # Step Functions -- data pipeline orchestration
]
