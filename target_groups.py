import boto3

session = lambda p,r: boto3.session.Session(profile_name=p, region_name=r)
check_healthy = lambda x: alb.describe_target_health(TargetGroupArn=x)

s = session("profile", "sa-east-1")
alb = s.client('elbv2')

target_groups =  alb.describe_target_groups()

for tg in target_groups['TargetGroups']:
    TargetGroupName = tg['TargetGroupName']
    TargetGroupArn = tg['TargetGroupArn']
    healthy = check_healthy(TargetGroupArn)
    for inst in healthy["TargetHealthDescriptions"]:
        State = inst["TargetHealth"]["State"]
        if State != "healthy" and State != "unused":
            print "TG Name: %s" % TargetGroupName
            print "%s: %s\n" % (inst["Target"]["Id"], State)
