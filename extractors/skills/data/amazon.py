from ..tag import Company, Skill, Tech
from ..utils import dis_context, dis_neighbours

dis_ctx = dis_context("amazon", "aws")

SKILLS: list[Skill] = [
  Company("Amazon", ["(@)amazon"]),

  Tech("AWS-CDK", ["aws=cdk", "cdk"], "Framework for defining and provisioning cloud IAC"),

  # AWS
  Tech("Amazon-WebServices", ["amazon-web=services", "aws"], "AWS"),
  Tech("Amazon-Athena", ["aws=athena"], "Analytics, ML + SQL over S3"),
  Tech("Amazon-Athena", ["athena"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Tech("Amazon-Aurora", ["aws=aurora"], "Managed DB"),
  Tech("Amazon-Aurora", ["aurora"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Tech("Amazon-Beanstalk", ["aws=beanstalk", "beanstalk"], "Webapp deployment"),
  Tech("Amazon-CloudFormation", ["aws=cloudformation", "cloudformation"], "IAC provisioning"),
  Tech("Amazon-CloudFront", ["aws=cloudfront", "cloudfront"], "CDN"),
  Tech("Amazon-CloudWatch", ["aws=cloudwatch", "cloudwatch"], "Monitoring umbrella"),
  Tech("Amazon-Cognito", ["aws=cognito", "cognito"], "Authentication and authorization for web and mobile applications"),
  Tech("Amazon-DynamoDB", ["aws=dynamo=db", "dynamo=db"], "Distributed NoSQL DB"),
  Tech("Amazon-EC2", ["aws=ec2", "ec2"], "Elastic compute cloud"),
  Tech("Amazon-ECS", ["aws=ecs", "ecs"], "Elastic container services"),
  Tech("Amazon-EBS", ["aws=ebs", "ebs"], "Elastic block store"),
  Tech("Amazon-EKS", ["aws=eks", "eks"], "Elastic kubernetes service"),
  Tech("Amazon-ElastiCache", ["aws=elasticache", "elasticache"], "Caching"),
  Tech("Amazon-Glue", ["aws=glue"], "Batch data ingestion, data pipeline orchestration"),
  Tech("Amazon-Glue", ["glue"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Tech("Amazon-IAM", ["aws=iam"], "Identity and access management"),
  Tech("Amazon-IAM", ["iam"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Tech("Amazon-Lambda", ["aws=lambda"], "Lambda service"),
  Tech("Amazon-Lambda", ["lambda"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Tech("Amazon-KMS", ["aws=kms"], "Streaming data ingestion & analytics"),
  Tech("Amazon-KMS", ["kms"], disambiguate=[
    dis_neighbours(),
    dis_ctx,
  ]),
  Tech("Amazon-Kinesis", ["aws=kinesis", "kinesis"], "Streaming data ingestion & analytics"),
  Tech("Amazon-Neptune", ["aws=neptune", "neptune"], "Graph DB"),
  Tech("Amazon-SNS", ["aws=sns", "sns"], "Simple notification service"),
  Tech("Amazon-SQS", ["aws=sqs", "sqs"], "Simple queue service"),
  Tech("Amazon-S3", ["aws=s3", "s3"], "Object storage"),
  Tech("Amazon-RDS", ["aws=rds", "rds"], "Relational database service"),
  Tech("Amazon-Redshift", ["aws=redshift", "redshift"], "Data warehouse & BI"),
  Tech("Amazon-SageMaker", ["aws=sagemaker", "sagemaker"], "Deploy ML"),
  Tech("Amazon-VPC", ["aws=vpc"], "Virtual private cloud"),
  Tech("Amazon-VPC", ["vpc"], disambiguate=[
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
