import os
import boto3
from fabric.api import run
from collections import defaultdict
from fabric.state import env
from fabric.tasks import execute


def validate():
    validate_cloudformation_files()


def validate_cloudformation_files():
    client = boto3.client('cloudformation')

    current_dir = os.path.dirname(__file__)
    cloudformation_dir = os.path.join(current_dir, 'cloudformation')
    cloudformation_files = []
    for (dirpath, dirnames, filenames) in os.walk(cloudformation_dir):
        cloudformation_files = [f for f in filenames if f.endswith('.json')]
        break

    for filename in cloudformation_files:
        print 'validating', filename
        file_path = os.path.join(cloudformation_dir, filename)
        template_body = open(file_path).read()
        client.validate_template(TemplateBody=template_body)


def create_stack(stack):
    validate()
    client = boto3.client('cloudformation')
    current_dir = os.path.dirname(__file__)
    cloudformation_dir = os.path.join(current_dir, 'cloudformation')
    template_path = os.path.join(cloudformation_dir, '%s.json' % stack)
    template_body = open(template_path).read()
    response = client.create_stack(
        StackName='stream-bench-%s' % stack, TemplateBody=template_body)
    print response


def delete_stack(stack):
    validate()
    client = boto3.client('cloudformation')
    response = client.delete_stack(StackName='stream-bench-%s' % stack)
    print response


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
    run('python run.py --start-users=10000 --max-users=10000000 --multiplier=2 --duration=10')


def run_bench(stack):
    '''
    Log into the RabbitMQ machine
    Execute python run.py with production settings
    '''
    instance_dict = get_ec2_instances(stack, logical_id='RabbitAutoScaling')
    execute(_run_bench, hosts=instance_dict['running'])