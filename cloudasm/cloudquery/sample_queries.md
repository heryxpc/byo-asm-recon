# Sample Queries
Taken from https://github.com/cloudquery/cloudquery/tree/main/plugins/source/aws/policies_v1

# VPC Default SG no access
```sql
select
  'The VPC default security group should not allow inbound and outbound traffic' as title,
  account_id,
  arn,
  case when
      group_name='default' 
      AND (jsonb_array_length(ip_permissions) > 0
      OR jsonb_array_length(ip_permissions_egress) > 0)
      then 'fail'
      else 'pass'
  end
from
    aws_ec2_security_groups;
```

# EC2 EBS default encryption enabled
```sql
select
  'EBS default encryption should be enabled' as title,
  account_id,
  concat(account_id,':',region) as resource_id,
  case when
    ebs_encryption_enabled_by_default is distinct from true
    then 'fail'
    else 'pass'
  end as status
from aws_ec2_regional_configs
```

# EC2 Instances with public IPs
```sql
select
    'EC2 instances should not have a public IP address' as title,
    account_id,
    instance_id as resource_id,
    case when
        public_ip_address is not null
        then 'fail'
        else 'pass'
    end as status
from aws_ec2_instances
```
# EC2 Security Groups
```sql
select
        account_id,
        region,
        group_name,
        arn,
        group_id as id,
        vpc_id,
        (i->>'FromPort')::integer AS from_port,
        (i->>'ToPort')::integer AS to_port,
        i->>'IpProtocol' AS ip_protocol,
        ip_ranges->>'CidrIp' AS ip,
        ip6_ranges->>'CidrIpv6' AS ip6
    from aws_ec2_security_groups, JSONB_ARRAY_ELEMENTS(aws_ec2_security_groups.ip_permissions) as i
    LEFT JOIN JSONB_ARRAY_ELEMENTS(i->'IpRanges') as ip_ranges ON true
    LEFT JOIN JSONB_ARRAY_ELEMENTS(i->'Ipv6Ranges') as ip6_ranges ON true;
```