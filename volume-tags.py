#!/usr/bin/env python
# raphael at rabeloo dot com dot br
import sys, re, optparse
import boto3

def main(argv):
    try:
        ec2 = conn(options.profile, options.region)
        instances = ec2.instances.all()

        for instance in instances:
            ec2 = conn(options.profile, options.region)
            root_volume_block = instance.block_device_mappings[0].get("Ebs", {}).get("VolumeId", None)
            instance_id = instance.id
            tags = [a for a in instance.tags if not re.findall("aws:*", a.get("Key", None))]
            volume = ec2.Volume(root_volume_block)
            
            stamp = confirm(root_volume_block, instance_id, tags)

            volume.create_tags(Tags=tags)

            if stamp == "y" or stamp == "Y":
                print 'Aplicando as atualizacoes... %s | %s' % (instance_id, root_volume_block)
                volume.create_tags(Tags=tags)
            elif stamp == "n" or stamp == "N":
                print "CANCELADO PELO USUARIO."
                sys.exit(1)
            else:
                print "Opcao incorreta. Terminando..."
                sys.exit(1)
            
    except Exception, e:
        print "Error: Verify profile and region"
        raise

def confirm(volume_id, instance_id, tags):
    print "+ [ Volume ID: %s | Instance ID: %s]" % (volume_id, instance_id) 
    for tag in tags:
        print "TAG: %s : %s" % (tag["Key"], tag["Value"])
        
    # print "As seguintes tags serao aplicacadas ao volume '%s' em uso pela instancia %s:" % (volume_id, instance_id, str(tags))
    # print "Tags:\n %s" % tags
    # stamp = raw_input("Deseja prosseguir? [y/n]: ")
    stamp = "y"
    return stamp


def conn(profile, region):
    ses = boto3.session.Session(profile_name=profile,region_name=region)
    return ses.resource('ec2')

parser = optparse.OptionParser()
parser.add_option('-p', '--profile', help='Profile of awscli credentials file to use.')
parser.add_option('-r', '--region', help='Profile of awscli credentials file to use.')
(options, args) = parser.parse_args()
mandatories = ['profile','region']

for m in mandatories:
    if not options.__dict__[m]:
        print "Mandatory option is missing.\n"
        parser.print_help()
        exit(-1)

if __name__ == "__main__":
    main(sys.argv[1:])