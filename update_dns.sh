#!/bin/bash
# by rabeloo
#
# Put in crontab:
# */5 * * * * /path/to/update_dns.sh
#
# Change if necessary:
AWS_DEFAULT_REGION="us-east-1"
AWS_DEFAULT_OUTPUT="text"
# Get the actual ip
ACTUAL_IP=$(curl http://curlmyip.com)
# Set your hostedzone and dns that you'll be updated
HOSTED_ZONE=""
DNS_NAME=""
# Execute awscli to update dns entry.
# You need permission to execute ChangeResourceRecordSets
update_return=$(aws route53 change-resource-record-sets --hosted-zone-id $HOSTED_ZONE --change-batch '{ "Changes": [ { "Action": "UPSERT", "ResourceRecordSet": { "Name": "'$DNS_NAME'", "Type": "A", "TTL": 60, "ResourceRecords": [ {"Value": "'$ACTUAL_IP'"} ] } } ] }')
