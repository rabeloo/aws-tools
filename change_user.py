#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import ConfigParser
import optparse, sys, os
from os.path import expanduser
from random import choice

def main(argv):
    try:
        if options.profile == 'all':
            for p in profiles:
                if options.create:
                    createUser(options.create, p)
                else:
                    changePass(options.update, p)
        else:
            if options.create:
                createUser(options.create, options.profile)
            else:
                changePass(options.update, options.profile)

    except Exception:
        print "Error: Verify if profile is typed correctly"
        raise

def genPass(length=16):
    charsets = [
    'abcdefghijklmnopqrstuvwxyz',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    '0123456789',
    '^!\$%&/()=?{[]}+~#-_.:,;<>|\\',
    ]
    pwd = []
    charset = choice(charsets)
    while len(pwd) < length:
        pwd.append(choice(charset))
        charset = choice(list(set(charsets) - set([charset])))
    return "".join(pwd)

def changePass(user, profile):
    password = genPass()
    try:
        sess = boto3.Session(region_name='us-east-1', profile_name=profile)
        iam = sess.client('iam')
        account_alias = iam.list_account_aliases()
        iam.update_login_profile(UserName=user, Password=password, PasswordResetRequired=True)
        print "%s\n%s\n%s" % (account_alias.get('AccountAliases'), user,password)
    except:
        raise
        pass

def createUser(user, profile):
    password = genPass()
    try:
        sess = boto3.Session(region_name='us-east-1', profile_name=profile)
        iam = sess.client('iam')
        account_alias = iam.list_account_aliases()
        iam.createUser(UserName=user)
        iam.add_user_to_group(GroupName='operations', UserName=user)
        iam.create_login_profile(UserName=user, Password=genPass(), PasswordResetRequired=True)
        print "%s\n%s\n%s" % (account_alias.get('AccountAliases'), user,password)
    except:
        raise
        pass

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
parser.add_option('-c', '--create', help='Create a new user')
parser.add_option('-u', '--update', help='User to change password')
# Mandatories parameters
(options, args) = parser.parse_args()
mandatories = ['profile']

for m in mandatories:
    if not options.__dict__[m]:
        print "Mandatory option is missing.\n"
        parser.print_help()
        sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
