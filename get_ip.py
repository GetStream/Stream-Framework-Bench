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
def connect(region):
    profile = metadata['iam']['info']['InstanceProfileArn']
    profile = profile[profile.find('/') + 1:]

    conn = boto.ec2.connection.EC2Connection(
            region=boto.ec2.get_region(region),
            aws_access_key_id=metadata['iam']['security-credentials'][profile]['AccessKeyId'],
            aws_secret_access_key=metadata['iam']['security-credentials'][profile]['SecretAccessKey'],
            security_token=metadata['iam']['security-credentials'][profile]['Token']
    )

    return conn


#
# Print out private IPv4
#
def print_ips(region, tag_name):
    conn = connect(region)
    reservations = conn.get_all_instances(filters={"tag:Name": tag_name})

    print("%s" % (reservations[0]["Instances"][0]["PrivateIpAddress"]))


#
# Main
#
opts, args = getopt.getopt(sys.argv[1:], "Lt:r:", ["tag-name", "region"])

for opt, arg in opts:
    if opt in ("-t", "--tag-name"):
        tag_name = arg
    elif opt in ("-r", "--region"):
        region = arg

print_ips(region, tag_name)
