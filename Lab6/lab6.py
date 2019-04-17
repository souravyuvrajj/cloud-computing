import boto3
import pprint
# Credentials & Region
access_key = "AKIAJERTBDC5Y7HANPGA"
secret_key = "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"
region = "ap-south-1"
EC2_KEY_HANDLE = "sourav"

# ECS Details
cluster_name = "BotoCluster3"
service_name = "service_hello_world"
task_name = "hello_world"


ecs_client = boto3.client(
    'ecs',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region,
)

ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

elb_client = boto3.client(
     'elb',
     aws_access_key_id=access_key,
     aws_secret_access_key=secret_key,
     region_name=region
)

print("Creating Cluster")
def launch_ecs_example():
    response = ecs_client.create_cluster(
        clusterName=cluster_name
    )
    pprint.pprint(response)
    print("-------------------------------------------------------------------------------------")


    response = ec2_client.run_instances(
        # Use the official ECS image
        ImageId="ami-0912f71e06545ad88",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
    )
    print("Creating an EC2 Instance")
    pprint.pprint(response)
    print("--------------------------------------------------------------------------")
    print("Creating a ELB ")
    response = elb_client.create_load_balancer(
    Listeners=[
        {
            'InstancePort': 80,
            'InstanceProtocol': 'HTTP',
            'LoadBalancerPort': 80,
            'Protocol': 'HTTP',
        },
    ],
    LoadBalancerName='my-load-balancer',
    SecurityGroups=[
        'sg-08c620a6d929e119b',
    ],
    Subnets=[
        'subnet-f8074690',
    ],
    )

    print(response)

    print("--------------------------------------------------------------------------")

    # Create a task definition
    print("Creating a task definition")
    response = ecs_client.register_task_definition(
        containerDefinitions=[
        {
          "name": "wordpress",
          "links": [
            "mysql"
          ],
          "image": "wordpress",
          "essential": True,
          "portMappings": [
            {
              "containerPort": 80,
              "hostPort": 80
            }
          ],
          "memory": 300,
          "cpu": 10
        },
        {
          "environment": [
            {
              "name": "MYSQL_ROOT_PASSWORD",
              "value": "password"
            }
          ],
          "name": "mysql",
          "image": "mysql",
          "cpu": 10,
          "memory": 300,
          "essential": True
        }
        ],
        family="hello_world"
    )

    pprint.pprint(response)
    print("---------------------------------------------------------------------------------------------")

    # Create service with exactly 1 desired instance of the task
    # Info: Amazon ECS allows you to run and maintain a specified number
    # (the "desired count") of instances of a task definition
    # simultaneously in an ECS cluster.

    response = ecs_client.create_service(
        cluster=cluster_name,
        serviceName=service_name,
        taskDefinition=task_name,
        desiredCount=1,
        clientToken='request_identifier_string',
        deploymentConfiguration={
            'maximumPercent': 200,
            'minimumHealthyPercent': 50
        }
    )

    pprint.pprint(response)
    print("---------------------------------------------------------------------------------------------")


# Shut everything down and delete task/service/instance/cluster
def terminate_ecs_example():
    try:
        # Set desired service count to 0 (obligatory to delete)
        response = ecs_client.update_service(
            cluster=cluster_name,
            service=service_name,
            desiredCount=0
        )
        # Delete service
        response = ecs_client.delete_service(
            cluster=cluster_name,
            service=service_name
        )
        pprint.pprint(response)
        print("---------------------------------------------------------------------------------------------")
    except:
        print("Service not found/not active")

    # List all task definitions and revisions
    response = ecs_client.list_task_definitions(
        familyPrefix=task_name,
        status='ACTIVE'
    )

    # De-Register all task definitions
    for task_definition in response["taskDefinitionArns"]:
        # De-register task definition(s)
        deregister_response = ecs_client.deregister_task_definition(
            taskDefinition=task_definition
        )
        pprint.pprint(deregister_response)
        print("---------------------------------------------------------------------------------------------")

    # Terminate virtual machine(s)
    response = ecs_client.list_container_instances(
        cluster=cluster_name
    )
    if response["containerInstanceArns"]:
        container_instance_resp = ecs_client.describe_container_instances(
            cluster=cluster_name,
            containerInstances=response["containerInstanceArns"]
        )
        for ec2_instance in container_instance_resp["containerInstances"]:
            ec2_termination_resp = ec2_client.terminate_instances(
                DryRun=False,
                InstanceIds=[
                    ec2_instance["ec2InstanceId"],
                ]
            )

    # Finally delete the cluster
    response = ecs_client.delete_cluster(
        cluster=cluster_name
    )
    pprint.pprint(response)
    print("---------------------------------------------------------------------------------------------")


launch_ecs_example()
terminate_ecs_example()
