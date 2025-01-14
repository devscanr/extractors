from ..skill import Skill
from ..utils import dis_context, dis_neighbours

dis_ctx = dis_context("amazon", "aws")

SKILLS: list[Skill] = [
  Skill("Amazon", ["(@)amazon"], "Company"),

  Skill("AWS-CDK", ["aws=cdk", "cdk"], "Framework for defining and provisioning cloud IAC"),

  # AWS
  Skill("Amazon-WebServices", ["amazon-web=services", "aws"], "AWS"),
  Skill("Amazon-Athena", ["aws=athena"], "Analytics, ML + SQL over S3"),
  Skill("Amazon-Athena", ["athena"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Skill("Amazon-Aurora", ["aws=aurora"], "Managed DB"),
  Skill("Amazon-Aurora", ["aurora"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Skill("Amazon-Beanstalk", ["aws=beanstalk", "beanstalk"], "Webapp deployment"),
  Skill("Amazon-CloudFormation", ["aws=cloudformation", "cloudformation"], "IAC provisioning"),
  Skill("Amazon-CloudFront", ["aws=cloudfront", "cloudfront"], "CDN"),
  Skill("Amazon-CloudWatch", ["aws=cloudwatch", "cloudwatch"], "Monitoring umbrella"),
  Skill("Amazon-Cognito", ["aws=cognito", "cognito"], "Authentication and authorization for web and mobile applications"),
  Skill("Amazon-DynamoDB", ["aws=dynamo=db", "dynamo=db"], "Distributed NoSQL DB"),
  Skill("Amazon-EC2", ["aws=ec2", "ec2"], "Elastic compute cloud"),
  Skill("Amazon-ECS", ["aws=ecs", "ecs"], "Elastic container services"),
  Skill("Amazon-EBS", ["aws=ebs", "ebs"], "Elastic block store"),
  Skill("Amazon-EKS", ["aws=eks", "eks"], "Elastic kubernetes service"),
  Skill("Amazon-ElastiCache", ["aws=elasticache", "elasticache"], "Caching"),
  Skill("Amazon-Glue", ["aws=glue"], "Batch data ingestion, data pipeline orchestration"),
  Skill("Amazon-Glue", ["glue"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Skill("Amazon-IAM", ["aws=iam"], "Identity and access management"),
  Skill("Amazon-IAM", ["iam"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Skill("Amazon-Lambda", ["aws=lambda"], "Lambda service"),
  Skill("Amazon-Lambda", ["lambda"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Skill("Amazon-KMS", ["aws=kms"], "Streaming data ingestion & analytics"),
  Skill("Amazon-KMS", ["kms"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Skill("Amazon-Kinesis", ["aws=kinesis", "kinesis"], "Streaming data ingestion & analytics"),
  Skill("Amazon-Neptune", ["aws=neptune", "neptune"], "Graph DB"),
  Skill("Amazon-SNS", ["aws=sns", "sns"], "Simple notification service"),
  Skill("Amazon-SQS", ["aws=sqs", "sqs"], "Simple queue service"),
  Skill("Amazon-S3", ["aws=s3", "s3"], "Object storage"),
  Skill("Amazon-RDS", ["aws=rds", "rds"], "Relational database service"),
  Skill("Amazon-Redshift", ["aws=redshift", "redshift"], "Data warehouse & BI"),
  Skill("Amazon-SageMaker", ["aws=sagemaker", "sagemaker"], "Deploy ML"),
  Skill("Amazon-VPC", ["aws=vpc"], "Virtual private cloud"),
  Skill("Amazon-VPC", ["vpc"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),

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
