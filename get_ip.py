#!/usr/bin/python
#
# Get private IPv4s for a given instance name.
#
import boto
import boto.ec2
import getopt
import sys


#
# Get the profile
#
def connect():
    metadata = boto.utils.get_instance_metadata()
    region = metadata['placement']['availability-zone'][:-1]

    for role in metadata['iam']['security-credentials'].keys():
        conn = boto.ec2.connection.EC2Connection(
                region=boto.ec2.get_region(region),
                aws_access_key_id=metadata['iam']['security-credentials'][role]['AccessKeyId'],
                aws_secret_access_key=metadata['iam']['security-credentials'][role]['SecretAccessKey'],
                security_token=metadata['iam']['security-credentials'][role]['Token']
        )
        break

    return conn

#
# Print out private IPv4
#
def print_ips(tag_name):
    conn = connect()
    reservations = conn.get_all_instances(filters={"tag:Name": tag_name})

    for r in reservations:
        for i in r.instances:
            if i.private_ip_address:
                print("%s" % (i.private_ip_address))


#
# Main
#
opts, args = getopt.getopt(sys.argv[1:], "Lt:", ["tag-name="])

tag_name = ""
region = ""
for opt, arg in opts:
    if opt in ("-t", "--tag-name"):
        tag_name = arg

print_ips(tag_name)