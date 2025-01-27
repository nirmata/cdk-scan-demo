from aws_cdk import (
    aws_ecs as ecs,
    aws_iam as iam,
    Stack,
)
from constructs import Construct

class MyEcsStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a Fargate Task Definition
        task_definition = ecs.TaskDefinition(
            self, "MyECSTaskDefinition",
            compatibility=ecs.Compatibility.FARGATE,
            cpu="256",
            memory_mib="512"
        )

        # Add a container to the task definition
        container = task_definition.add_container(
            "MyContainer",
            image=ecs.ContainerImage.from_registry("ecr.io/amazon/amazon-ecs-sample"),
            logging=ecs.LogDriver.aws_logs(stream_prefix="MyApp"),
            readonly_root_filesystem=True
        )

        # Optionally, add port mappings now
        container.add_port_mappings(
            ecs.PortMapping(
                container_port=80
            )
        )

