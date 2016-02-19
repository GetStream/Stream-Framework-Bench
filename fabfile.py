import os
import boto3


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
    response = client.create_stack(StackName='stream-bench-%s' % stack, TemplateBody=template_body)
    print response
    
    
def delete_stack(stack):
    validate()
    client = boto3.client('cloudformation')
    response = client.delete_stack(StackName='stream-bench-%s' % stack)
    print response
        
        
