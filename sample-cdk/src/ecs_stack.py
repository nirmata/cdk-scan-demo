from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    RemovalPolicy
)
from constructs import Construct

class EcsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        # Create ECR Repository
        repository = ecr.Repository(
            self, 
            "MyRepository",
            repository_name="my-app-repo",
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create ECS Cluster
        cluster = ecs.Cluster(
            self, 
            "MyCluster",
            vpc=vpc
        )

        # Create Task Definition
        task_definition = ecs.FargateTaskDefinition(
            self, 
            "MyTaskDefinition",
            memory_limit_mib=512,
            cpu=256
        )

        # Add container to task definition
        task_definition.add_container(
            "MyContainer",
            image=ecs.ContainerImage.from_ecr_repository(repository),
            port_mappings=[ecs.PortMapping(container_port=80)]
        )

        # Create Fargate Service
        ecs.FargateService(
            self, 
            "MyService",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=2
        )