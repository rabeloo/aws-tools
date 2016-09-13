import boto3, json, urllib2
# raphael at rabeloo dot com dot br
# Getting instance informations to make a boto connection
getDoc = json.loads(urllib2.urlopen('http://169.254.169.254/latest/dynamic/instance-identity/document/').read())
region = getDoc["region"]
instanceId = getDoc["instanceId"]
privateIp = getDoc["privateIp"]
availabilityZone = getDoc["availabilityZone"]
## Make boto connection
ec2 = boto3.client("ec2", region_name=region)
# Get instance informations
instInfo = ec2.describe_tags(Filters=[ { 'Name' : 'resource-id', 'Values': [ instanceId ] }, ])
# Verify if instance has tag, and tag 'Name'
if instInfo.has_key("Tags"):
    instTags = instInfo["Tags"]
    for tag in instTags:
        if tag.get('Key') == 'Name':
            tagNameOld = tag.get('Value')
else:
    print "The instance %s doesn't has any tag." % instanceId
# Get last ip octet to compose new instance name
lastOctet = privateIp.split('.')[-1]
# Verify Availabiliy zone to compose instance name
instAz = availabilityZone[-1:]
# Generate the new tag 'Name' of the ec2 instance
tagName = "%s-%s%s" % (tagNameOld,lastOctet,instAz)
# Rename tag 'Name' with the new instance name
ec2.create_tags(Resources=[ instanceId ], Tags=[ { 'Key': 'Name', 'Value': tagName } ])
# Print tag name (used by ansible hostname variable)
print tagName
