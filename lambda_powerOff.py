import boto3

ec2 = boto3.resource('ec2')

def lambda_handler(event, context):

    filters = [{
            'Name': 'tag:AutoOff',
            'Values': ['True']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]

    instances = ec2.instances.filter(Filters=filters)
    runInstances = [ instance.id for instance in instances ]

    if len(runInstances) > 0:
        powerOff = ec2.instances.filter(InstanceIds=runInstances).stop()
        print powerOff
    else:
        print "No instances poweroff"
