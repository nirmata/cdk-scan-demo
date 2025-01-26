from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecs_patterns as ecs_patterns,
    core
)

class ECSFargateStack(Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create VPC
        vpc = ec2.Vpc(self, "MyVPC", max_azs=2)

        # Create ECS Cluster
        cluster = ecs.Cluster(
            self, 
            "MyCluster",
            vpc=vpc
        )

        # Define task definition
        task_definition = ecs.FargateTaskDefinition(
            self, 
            "MyTaskDefinition",
            memory_limit_mib=2048,
            cpu=1024
        )

        # Add container to task definition
        task_definition.add_container(
            "AppContainer",
            image=ecs.ContainerImage.from_registry("nginx:latest"),
            port_mappings=[ecs.PortMapping(container_port=80)]
        )

        # Create Fargate service with load balancer
        ecs_patterns.ApplicationLoadBalancedFargateService(
            self, 
            "MyFargateService",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=2,
            public_load_balancer=True
        )

app = core.App()
ECSFargateStack(app, "ECSDeploymentStack")
app.synth()