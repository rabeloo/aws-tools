#!/usr/bin/env python
## Generate a template to AWS CloudFormation
## Author: Raphael Rabelo
## raphael at rabeloo dot com dot br

import json

format = {}
format['AWSTemplateFormatVersion'] = '2010-09-09'
format['Description'] = 'My simple ec2 stack with IAM Role and ELB'
format['Parameters'] = {}
format['Parameters']['KeyName']={}
format['Parameters']['KeyName']['Description'] = 'Name of an existing EC2 KeyPair to enable SSH access to the instance'
format['Parameters']['KeyName']['Type'] = 'String'
format['Parameters']['KeyName']['Default'] = '<INSERT_KEYNAME_HERE>'
format['Parameters']['KeyName']['AllowedValues'] = ["<KEY_1>", "<KEY_2>"]
format['Parameters']['InstanceType'] = {}
format['Parameters']['InstanceType']['Description'] = 'WebServer for redirects in EC2 instance type'
format['Parameters']['InstanceType']['Type'] = 'String'
format['Parameters']['InstanceType']['Default'] = 't2.micro'
format['Parameters']['InstanceType']['AllowedValues'] = ["t2.micro","m3.medium","m3.large","m3.xlarge"]
format['Parameters']['InstanceType']['ConstraintDescription'] = 'must be a valid EC2 instance type.'
format['Mappings'] = {}
format['Mappings']['RegionMap'] = {}
format['Mappings']['RegionMap']['us-east-1'] = {}
format['Mappings']['RegionMap']['us-east-1']['baseAMI'] = '<INSERT_AMI_ID>'
format['Mappings']['RegionMap']['us-east-1']['SGId'] = '<INSERT_SG>'
format['Mappings']['RegionMap']['us-east-1']['SubnetId'] = '<INSERT_SUBNET_ID>'

# Resources
format['Resources'] = {}
## Create ELB with 2 Listeners
format['Resources']['ELB'] = {}
format['Resources']['ELB']['Type'] = 'AWS::ElasticLoadBalancing::LoadBalancer'
format['Resources']['ELB']['Properties'] = {}
format['Resources']['ELB']['Properties']['Scheme'] = 'internet-facing'
format['Resources']['ELB']['Properties']['SecurityGroups'] = ["<INSERT_ELB_SG>"]
format['Resources']['ELB']['Properties']['Subnets'] = ["<INSERT_SUBNET_AZ1>", "<INSERT_SUBNET_AZ2>"]
format['Resources']['ELB']['Properties']['Instances'] = [{"Ref":"MyInstance"}]
elb_80={"LoadBalancerPort": "80","InstancePort": "80","Protocol": "TCP"}
elb_443={}
elb_443['InstancePort'] = '80'
elb_443['InstanceProtocol'] = 'HTTP'
elb_443['LoadBalancerPort'] = '443'
elb_443['Protocol'] = 'HTTPS'
elb_443['SSLCertificateId'] = '<INSERT_YOUR_SSL_CERTIFICATE_SSL_ARN>'
format['Resources']['ELB']['Properties']['Listeners'] = [elb_80, elb_443]
format['Resources']['ELB']['Properties']['HealthCheck'] = {}
format['Resources']['ELB']['Properties']['HealthCheck']['Target'] = 'TCP:80'
format['Resources']['ELB']['Properties']['HealthCheck']['HealthyThreshold'] = '3'
format['Resources']['ELB']['Properties']['HealthCheck']['UnhealthyThreshold'] = '2'
format['Resources']['ELB']['Properties']['HealthCheck']['Interval'] = '12'
format['Resources']['ELB']['Properties']['HealthCheck']['Timeout'] = '3'
format['Resources']['ELB']['Properties']['ConnectionDrainingPolicy'] = {"Enabled" : "true","Timeout" : "300"}

## Resource: IAMRole
format['Resources']['IAMRole'] = {}
format['Resources']['IAMRole']['Type'] = 'AWS::IAM::Role'
format['Resources']['IAMRole']['Properties'] = {}
format['Resources']['IAMRole']['Properties']['AssumeRolePolicyDocument'] = {}
format['Resources']['IAMRole']['Properties']['AssumeRolePolicyDocument']['Version'] = '2012-10-17'
stmt_content = {}
stmt_content['Effect'] = 'Allow'
stmt_content['Principal'] = {'Service':["ec2.amazonaws.com",]}
stmt_content['Action'] = ["sts:AssumeRole",]
AssumePolicy_Statement = []
AssumePolicy_Statement.append(stmt_content)
format['Resources']['IAMRole']['Properties']['AssumeRolePolicyDocument']['Statement'] = [AssumePolicy_Statement[0]]
format['Resources']['IAMRole']['Properties']['Path'] = '/'

## Resource: IAMPolicy
format['Resources']['IAMPolicy'] = {}
format['Resources']['IAMPolicy']['Type'] = 'AWS::IAM::Policy'
format['Resources']['IAMPolicy']['Properties'] = {}
format['Resources']['IAMPolicy']['Properties']['PolicyName'] = 'bootstrap'
format['Resources']['IAMPolicy']['Properties']['PolicyDocument'] = {}
format['Resources']['IAMPolicy']['Properties']['PolicyDocument']['Version'] = '2012-10-17'
iam_ec2_content = {}
iam_ec2_content['Effect'] = 'Allow'
iam_ec2_content['Action'] = ["ec2:DescribeTags",]
iam_ec2_content['Resource'] = ["*",]
ec2_policy = []
ec2_policy.append(iam_ec2_content)
iam_route53_content = {}
iam_route53_content['Effect'] = 'Allow'
iam_route53_content['Action'] = ["route53:ListHostedZones", "route53:ChangeResourceRecordSets",]
iam_route53_content['Resource'] = ["*",]
route53_policy = []
route53_policy.append(iam_route53_content)
format['Resources']['IAMPolicy']['Properties']['PolicyDocument']['Statement'] = [ec2_policy[0], route53_policy[0]]
format['Resources']['IAMPolicy']['Properties']['Roles'] = [{"Ref":"IAMRole"},]

## Resource: IAMInstanceProfile
format['Resources']['IAMInstanceProfile'] = {}
format['Resources']['IAMInstanceProfile']['Type'] = 'AWS::IAM::InstanceProfile'
format['Resources']['IAMInstanceProfile']['Properties'] = {}
format['Resources']['IAMInstanceProfile']['Properties']['Path'] = "/"
format['Resources']['IAMInstanceProfile']['Properties']['Roles'] = [{"Ref":"IAMRole"}]

## Resource: MyInstance
format['Resources']['MyInstance'] = {}
format['Resources']['MyInstance']['Type'] = 'AWS::EC2::Instance'
### MyInstance Metadata
format['Resources']['MyInstance']['Metadata'] = {}
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init'] = {}
### Configuring configSets order
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configSets'] = {}
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configSets']['InstallandRun'] = ["install", "configure"]
### install configset
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['install'] = {}
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['install']['Packages'] = {}
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['install']['Packages']['yum'] = {"git":[],"wget":[],}
### configure configset
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configure'] = {}
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configure']['files'] = {}
#### File: example.txt
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configure']['files']['/tmp/example.txt'] = {}
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configure']['files']['/tmp/example.txt']['content'] = {}
##### Write your file using an array and put  \n in the final of line.
example_text=["This is only an example\n", "You can write anything here\n", "cf-template by rabeloo\n"]
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configure']['files']['/tmp/example.txt']['content']['Fn::Join'] = ["",example_text,]
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configure']['files']['/tmp/example.txt']['mode'] = '000644'
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configure']['files']['/tmp/example.txt']['owner'] = 'root'
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configure']['files']['/tmp/example.txt']['group'] = 'root'
### configure commands
format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configure']['commands'] = {}
cmds = []
cmds.append('echo "Put your comand here."')
cmds.append('echo "You can some commands you wants, the next loop will generate the order correctly."')
for num in range(0,1):
  format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configure']['commands'][num+1] = {}
  format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configure']['commands'][num+1]['command'] = cmds[num]
  format['Resources']['MyInstance']['Metadata']['AWS::CloudFormation::Init']['configure']['commands'][num+1]['ignoreErrors'] = 'true'

### MyInstance Properties
format['Resources']['MyInstance']['Properties'] = {}
format['Resources']['MyInstance']['Properties']['AvailabilityZone'] = '<PUT_THE_AZ_HERE>'
format['Resources']['MyInstance']['Properties']['DisableApiTermination'] = 'false'
img_content = {}
img_content['Fn::FindInMap'] = ["RegionMap", {"Ref": "AWS::Region"}, "baseAMI",]
Imgid = []
Imgid.append(img_content)
format['Resources']['MyInstance']['Properties']['ImageId'] = Imgid[0]
format['Resources']['MyInstance']['Properties']['InstanceType'] = {"Ref" : "InstanceType"}
format['Resources']['MyInstance']['Properties']['IamInstanceProfile'] = {"Ref" : "IAMInstanceProfile"}
format['Resources']['MyInstance']['Properties']['KeyName'] = {"Ref" : "KeyName"}
sg_content = {}
sg_content['Fn::FindInMap'] = ["RegionMap", {"Ref": "AWS::Region"}, "SGId",]
SGgrp = []
SGgrp.append(sg_content)
format['Resources']['MyInstance']['Properties']['SecurityGroupIds'] = [SGgrp[0]]
sbnet_content = {}
sbnet_content['Fn::FindInMap'] = ["RegionMap", {"Ref": "AWS::Region"}, "SubnetId",]
Subnet = []
Subnet.append(sbnet_content)
format['Resources']['MyInstance']['Properties']['SubnetId'] = Subnet[0]
tags_content = {}
tags_content['Key'] = 'Name'
tags_content['Value'] = 'my-cf-instance'
Tags = []
Tags.append(tags_content)
format['Resources']['MyInstance']['Properties']['Tags'] = [Tags[0]]

### UserData
#### The commands below are necessaries to install cfn-init, this will run you Metadata content correctly.
format['Resources']['MyInstance']['Properties']['UserData'] = {}
format['Resources']['MyInstance']['Properties']['UserData']['Fn::Base64'] = {}
userdata_content=[ "#!/bin/bash\n","yum clean all\n","yum install pystache python-daemon -y\n","/bin/rpm -U https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.amzn1.noarch.rpm\n","/opt/aws/bin/cfn-init ","         --stack ",
    {"Ref":"AWS::StackName"},"         --resource MyInstance ","         --configsets InstallandRun","         --region ",{"Ref":"AWS::Region"},"\n" ]
format['Resources']['MyInstance']['Properties']['UserData']['Fn::Base64']['Fn::Join'] = ["", userdata_content]

## Print JSON Template
print json.dumps(format, indent=2, sort_keys=False, ensure_ascii=False)
