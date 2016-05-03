#!/usr/bin/env python
# raphael at rabeloo dot com dot br
import boto3
import ConfigParser, optparse, sys, os
from colorama import Fore, Back, Style
from os.path import expanduser

regions =   [
             'sa-east-1',
             'us-east-1',
             'us-west-1',
             'us-west-2',
             'ap-northeast-1',
             'ap-southeast-1',
             'ap-southeast-2',
             'eu-central-1',
             'eu-west-1'
            ]

def main(argv):
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
    print "Searching instances in %s: %s" % (profile, region)
    for i in ec2.instances.all():
        if i.tags is None:
            continue
        for t in i.tags:
            if t['Key'] == 'Name':
                printing(profile, region, i.state['Name'], i.instance_type, t['Value'], i.id, i.private_ip_address)

def printing(profile, region, state, inst_type, tag_name, inst_id, inst_privip):
    output = "{0} : {1} : {2} ({3}) : {4} : {5}".format(profile, region, tag_name, inst_id, inst_type, inst_privip)
    pstate = "[{0}]".format(state)
    if state == "running":
        print(Style.BRIGHT + Fore.GREEN + pstate + Style.RESET_ALL),
        print(Style.BRIGHT + output + Style.RESET_ALL)

    else:
        print(Fore.RED + pstate + Style.RESET_ALL),
        print output

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
