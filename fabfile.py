import os
import boto3
from fabric.api import run
from collections import defaultdict
from fabric.state import env
from fabric.tasks import execute
from fabric.operations import sudo
import time
import botocore

BENCHMARK_REGION = 'us-west-2'
BASE_DIR = os.path.dirname(__file__)
CLOUDFORMATION_DIR = os.path.join(BASE_DIR, 'cloudformation')
    

def validate():
    validate_cloudformation_files()
    
    
def read_available_templates():
    cloudformation_templates = {}
    cloudformation_files = []
    for (dirpath, dirnames, filenames) in os.walk(CLOUDFORMATION_DIR):
        cloudformation_files = [f for f in filenames if f.endswith('.template')]
        break
    for filename in cloudformation_files:
        name = filename.split('.')[0]
        cloudformation_templates[filename] = read_template(name)
    return cloudformation_templates

def read_template(name):
    current_dir = os.path.dirname(__file__)
    cloudformation_dir = os.path.join(current_dir, 'cloudformation')
    template_path = os.path.join(cloudformation_dir, '%s.template' % name)
    template_body = open(template_path).read()
    return template_body


def validate_cloudformation_files():
    client = boto3.client('cloudformation')
    cloudformation_templates = read_available_templates()

    for name, template_body in cloudformation_templates.items():
        print 'validating', name
        client.validate_template(TemplateBody=template_body)


def create_stack(stack, datadog='none'):
    validate()
    client = boto3.client('cloudformation', region_name=BENCHMARK_REGION)
    template_body = read_template(stack)
    _wait_for_stack(stack)
    response = client.create_stack(
        StackName='stream-bench-%s' % stack, TemplateBody=template_body, Parameters=[{
            'ParameterKey': 'DatadogAPIKey',
            'ParameterValue': datadog,
            'UsePreviousValue': True
        }],
        Capabilities=[
            'CAPABILITY_IAM',
        ])
    print response
    _wait_for_stack(stack)
    print 'stack is ready, cloud-init will still take a while to install libs'


def delete_stack(stack):
    validate()
    client = boto3.client('cloudformation', region_name=BENCHMARK_REGION)
    _wait_for_stack(stack)
    response = client.delete_stack(StackName='stream-bench-%s' % stack)
    print response
    _wait_for_stack(stack)
    

def _wait_for_stack(stack):
    '''
    Wait till the stack is no longer in an in-progress state
    '''
    stack_name = 'stream-bench-%s' % stack
    cloudformation = boto3.resource('cloudformation', region_name=BENCHMARK_REGION)
    for x in range(30):
        try:
            stack_instance = cloudformation.Stack(stack_name)
            if 'PROGRESS' not in stack_instance.stack_status:
                return stack_instance
            print 'waiting for stack', stack_instance.stack_name, stack_instance.stack_status
            time.sleep(5)
        except botocore.exceptions.ClientError as e:
            return None
        

def get_ec2_instances(stack, logical_id):
    client = boto3.client('ec2')
    tags = {
        'tag:aws:cloudformation:stack-name': 'stream-bench-%s' % stack,
        'tag:aws:cloudformation:logical-id': logical_id
    }
    
    # create the filters
    filters = []
    for tag_name, tag_value in tags.items():
        filter = {'Name': tag_name, 'Values': [tag_value]}
        filters.append(filter)
        
    reservations = client.describe_instances(Filters=filters)['Reservations']
    instance_dict = defaultdict(list)
    
    for r in reservations:
        for i in r['Instances']:
            instance_dict[i['State']['Name']].append(i['PublicDnsName'])

    return instance_dict


def _run_bench():
    sudo('ENVIRONMENT=production python /srv/bench/sfb/run.py --start-users=10000 --max-users=10000000 --multiplier=2 --duration=10')


def _verify_rabbit():
    sudo('rabbitmqctl status')
    
    
def _verify_celery():
    sudo('ps aux | grep celery')
    
def _verify_cloud_init():
    sudo('ls -la /var/lib/cloud/instance/boot-finished')


def run_bench(stack):
    '''
    Log into the RabbitMQ machine
    Execute python run.py with production settings
    '''
    env.user = 'ubuntu'
    # check if rabbit and celery started correctly
    instance_dict = get_ec2_instances(stack, logical_id='RabbitAutoScaling')
    execute(_verify_rabbit, hosts=instance_dict['running'])
    execute(_verify_cloud_init, hosts=instance_dict['running'])
    celery_instance_dict = get_ec2_instances(stack, logical_id='CeleryAutoScaling')
    execute(_verify_celery, hosts=celery_instance_dict['running'])
    # start the actual benchmark
    execute(_run_bench, hosts=instance_dict['running'])
    
    
    
    
    