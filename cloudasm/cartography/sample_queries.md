# Sample Queries
## List all EC2 instances
```cypher
match (a:AWSAccount)-[r:RESOURCE]->(e:EC2Instance)
return a.id as account_id, a.name as account_name, e.instancetype as instance_type, size(collect(e.instancetype)) as instance_count, e.lastupdated order by account_name, instance_count desc
```
## List all EC2 instances and their assumable roles
```cypher
    match (e:EC2Instance)-[:STS_ASSUMEROLE_ALLOW]->(r:AWSRole) return e, r limit 30
```
## List all EC2 instances and their shared assumable roles
```cypher
    match (e:EC2Instance)-[:STS_ASSUMEROLE_ALLOW]->(r:AWSRole)<-[:STS_ASSUMEROLE_ALLOW]-(i:EC2Instance) return r.arn, e.id, e.instancetype order by r.arn desc limit 30
```
## What roles have permissions to EKS
```cypher
   match (r:AWSRole{name:'admin-deploys'})--(pol:AWSPolicy)--(stmt:AWSPolicyStatement) where any(x in stmt.action where x contains 'eks') return * limit 30;
```

## List all S3 buckets and their S3ACLs
```cypher
    MATCH (s:S3Bucket)-[]-(a:S3Acl) return s,a
```
## What S3 buckets have a policy granting anonymous access
```cypher
   MATCH (s:S3Bucket) where s.anonymous_access = true return s
```
## List all VPCs that are peered with the Zimride AWS account
```cypher
MATCH (other_account:AWSAccount)-[:RESOURCE]->(other_vpc:AWSVpc)-[:BLOCK_ASSOCIATION]->(other_block:AWSCidrBlock)-[:VPC_PEERING]-(aws_block:AWSCidrBlock)<-[:BLOCK_ASSOCIATION]-(aws_vpc:AWSVpc)<-[:RESOURCE]-(aws_account:AWSAccount)
WHERE other_account.id <> aws_account.id
RETURN other_account.name, other_account.id, other_vpc.vpcid, other_block.cidr_block, other_block.association_id, aws_block.cidr_block, aws_block.association_id, aws_vpc.vpcid ORDER BY other_account.name, other_account.cidr_block
```

## Find everything about an IP Address
```cypher
MATCH (n:EC2PrivateIp)-[r]-(n2)
WHERE n.public_ip = $neodash_ip
return n, r, n2

UNION MATCH(n:EC2Instance)-[r]-(n2)
WHERE n.publicipaddress = $neodash_ip
return  n, r, n2

UNION MATCH(n:NetworkInterface)-[r]-(n2)
WHERE n.public_ip = $neodash_ip
return n, r, n2

UNION MATCH(n:ElasticIPAddress)-[r]-(n2)
WHERE n.public_ip = $neodash_ip
return n, r, n2
```

## Which ELB LoadBalancers are internet accessible?¶
```cypher
MATCH (elb:LoadBalancer{exposed_internet: true})—->(listener:ELBListener)
RETURN elb.dnsname, listener.port
ORDER by elb.dnsname, listener.port
```

## How many unencrypted RDS instances are there?
```cypher
MATCH (a:AWSAccount)-[:RESOURCE]->(rds:RDSInstance)
WHERE rds.storage_encrypted = false
return a.name as AWSAccount, count(rds) as UnencryptedInstances
```

## Query all open ports via ELB
```cypher
    MATCH (dns:AWSDNSRecord)-[:DNS_POINTS_TO]->(lb)
    WHERE lb.scheme = "internet-facing"
    MATCH (lb)-[:MEMBER_OF_EC2_SECURITY_GROUP]->(sg:EC2SecurityGroup)
    MATCH (sg)<-[:MEMBER_OF_EC2_SECURITY_GROUP]-(ipi:IpPermissionInbound)
    MATCH (ipi)<--(ir:IpRange)
    WHERE ir.range = "0.0.0.0/0" AND ipi.toport <> 443 AND ipi.toport <> 80 AND ipi.toport <> -1
    RETURN DISTINCT ipi.toport as port, dns.name as `dnsname`
```
## Query all open ports via ELBv2
```cypher
    MATCH(d:AWSDNSRecord)-[:DNS_POINTS_TO]->(lb:LoadBalancerV2)
    MATCH (lb)-[:ELBV2_LISTENER]->(l:ELBV2Listener)
    WHERE lb.scheme = "internet-facing"
    RETURN DISTINCT l.port as port, d.name as `dnsname`
```