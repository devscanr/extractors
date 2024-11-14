from ..utils import Skill, contextual, contextual_or_neighbour

__all__ = ["SKILLS"]

ctx = contextual("Amazon")
ctxn = contextual_or_neighbour(["Amazon"], 2)

SKILLS: list[Skill] = [
  Skill("Amazon", ["amazon"], ""), # company (etc)

  # AWS
  Skill("Amazon-WebServices", ["amazon-web=services", "aws"], ""),
  Skill("Amazon-Athena", ["aws=athena"], ""), # analytics, ML + SQL over S3
  Skill("Amazon-Athena", ["athena"], "", disambiguate=ctx),             # /
  Skill("Amazon-Aurora", ["aws=aurora"], ""), # managed DB
  Skill("Amazon-Aurora", ["aurora"], "", disambiguate=ctx),             # /
  Skill("Amazon-Beanstalk", ["aws=beanstalk", "beanstalk"], ""), # webapp deployment
  Skill("Amazon-CloudFront", ["aws=cloudfront", "cloudfront"], ""), # CDN
  Skill("Amazon-CloudWatch", ["aws=cloudwatch", "cloudwatch"], ""), # monitoring umbrella
  Skill("Amazon-DynamoDB", ["aws=dynamo=db", "dynamo=db"], ""), # distributed NoSQL DB
  Skill("Amazon-EC2", ["aws=ec2", "ec2"], ""), # elastic compute cloud
  Skill("Amazon-ECS", ["aws=ecs", "ecs"], ""), # elastic container services
  Skill("Amazon-EBS", ["aws=ebs", "ebs"], ""), # elastic block store
  Skill("Amazon-EKS", ["aws=eks", "eks"], ""), # elastic kubernetes service
  Skill("Amazon-ElastiCache", ["aws=elasticache", "elasticache"], ""), # caching
  Skill("Amazon-Glue", ["aws=glue"], ""), # batch data ingestion, data pipeline orchestration
  Skill("Amazon-Glue", ["glue"], "", disambiguate=ctx),           # /
  Skill("Amazon-IAM", ["aws=iam"], ""), # identity and access management
  Skill("Amazon-IAM", ["iam"], "", disambiguate=ctx),          # /
  Skill("Amazon-Lambda", ["aws=lambda"], ""), # lambda
  Skill("Amazon-Lambda", ["lambda"], "", disambiguate=ctx),             # /
  Skill("Amazon-KMS", ["aws=kms"], ""), # streaming data ingestion & analytics
  Skill("Amazon-KMS", ["kms"], "", disambiguate=ctx),          # /
  Skill("Amazon-Kinesis", ["aws=kinesis", "kinesis"], ""), # streaming data ingestion & analytics
  Skill("Amazon-Neptune", ["aws=neptune", "neptune"], ""), # graph db
  Skill("Amazon-SNS", ["aws=sns", "sns"], ""), # simple notification service
  Skill("Amazon-SQS", ["aws=sqs", "sqs"], ""), # simple queue service
  Skill("Amazon-S3", ["aws=s3", "s3"], ""),     # object storage
  Skill("Amazon-RDS", ["aws=rds", "rds"], ""), # relational database service
  Skill("Amazon-Redshift", ["aws=redshift", "redshift"], ""), # data warehouse & BI
  Skill("Amazon-SageMaker", ["aws=sagemaker", "sagemaker"], ""), # deploy ML
  Skill("Amazon-VPC", ["aws=vpc"], ""), # virtual private cloud
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
