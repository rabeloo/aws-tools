#!/usr/bin/env bash˜
region=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone | sed 's|.$||g')
instance_id=$(curl -s http://169.254.169.254/latest/meta-data/instance-id/)
tag_name=$(aws ec2 describe-tags --filters Name=resource-type,Values=instance Name=resource-id,Values=$instance_id Name=key,Values=Name --region $region --output text | cut -f5)
instance_alias=$(echo ${tag_name} | gawk 'match($0,/(.*)\.aws.*/,cap)  {print cap[1]}')

domain=$(echo ${tag_name} | gawk 'match($1,/(.*)\.aws.*/,cap)  {print cap[1]}')

pattern=$(echo $instance_alias | sed 's/..$//g')
instance_count=$(aws ec2 describe-tags --filters Name=resource-type,Values=instance Name=key,Values=Name --region $region --output text | cut -f5 | grep $pattern | wc -l)

echo -ne "Pattern:\t$pattern\n"

if [ -z $instance_count ] || [ $instance_count -le 1 ]; then
        new_tag="${pattern}01"
elif [ $instance_count -ge 1 ]; then
        seq=$(($instance_count+1))
        seq2=$(printf %02d "$seq")
        new_tag="${pattern}${seq2}"
else
        echo "This is a unknown error!"
        exit 1
fi

echo -ne "New instance tag name:\t$new_tag\n"
