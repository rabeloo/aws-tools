#!/usr/bin/env python
# raphael at rabeloo dot com dot br
import boto3
import ConfigParser, optparse, sys, os
from os.path import expanduser

file = open("/Users/rabelo/.ssh/config.d/30_config-aws.conf", "w")

regions =   [
             'sa-east-1',
             'us-east-1',
            ]

def main(argv):
    print "Generating AWS Config file for ssh. Please wait..."
    try:
        if options.profile == 'all':
            for p in profiles:
                for region in regions:
                    ls(p, region)
        else:
            for region in regions:
                ls(options.profile, region)

    except Exception, e:
        print "Error: Verify if profile is typed correctly"
        raise

def init_session(profile, region):
    ses = boto3.session.Session(profile_name=profile,region_name=region)
    return ses.resource('ec2')

def ls(profile, region):
    ec2 = init_session(profile, region)
    for inst in ec2.instances.all():
        if inst.state["Name"] == "running":
            try:
                if inst.tags is None:
                    continue
                for tag in inst.tags:
                    if tag['Key'] == 'Name':
                        printing(tag['Value'], inst.private_ip_address)
            except:
                continue

def printing(tag_name, inst_privip):
    output = "Host {0}\n  Hostname {1}\n  User inf_roliveira\n\n".format(tag_name.lower(), inst_privip)
    file.write(output)

# Looking for profiles in credentials file
profiles = []
credentials_file = expanduser("~/.aws/credentials")
parser = ConfigParser.ConfigParser()
parser.read(credentials_file)
for p in parser.sections():
    if p.find("bp-") != -1:
        profiles.append(p)

# Parameters
parser = optparse.OptionParser()
parser.add_option('-p', '--profile', help='Profile of awscli credentials file to use.')
# Mandatories parameters
(options, args) = parser.parse_args()
mandatories = ['profile']

for m in mandatories:
    if not options.__dict__[m]:
        print "Mandatory option is missing.\n"
        parser.print_help()
        exit(-1)

if __name__ == "__main__":
    main(sys.argv[1:])
