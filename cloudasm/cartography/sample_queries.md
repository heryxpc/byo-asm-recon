# Sample Queries
## List all EC2 instances
```cypher
match (a:AWSAccount)-[r:RESOURCE]->(e:EC2Instance)
return a.id as account_id, a.name as account_name, e.instancetype as instance_type, size(collect(e.instancetype)) as instance_count, datetime({epochseconds:e.lastupdated}) as last_updated order by account_name, instance_count desc
```

## Which ELB LoadBalancers are internet accessible?
```cypher
MATCH (elb:LoadBalancer{exposed_internet: true})—->(listener:ELBListener)
RETURN elb.dnsname, listener.port
ORDER by elb.dnsname, listener.port
```

## Query open ports and Security Groups
```cypher
    MATCH (open)-[:MEMBER_OF_EC2_SECURITY_GROUP]->(sg:EC2SecurityGroup)
    MATCH (sg)<-[:MEMBER_OF_EC2_SECURITY_GROUP]-(ipi:IpPermissionInbound)
    MATCH (ipi)<--(ir:IpRange)
    WHERE ir.range = "0.0.0.0/0"
    OPTIONAL MATCH (dns:AWSDNSRecord)-[:DNS_POINTS_TO]->(lb)
    WHERE open.scheme = "internet-facing"
    RETURN DISTINCT ipi.toport as port, open.id, sg.id
```

## Query all open ports via ELB or ELBv2
```cypher
    MATCH (elb:LoadBalancer{exposed_internet: true})—->(listener:ELBListener)
    RETURN DISTINCT elb.dnsname as dnsname, listener.port as port 
    UNION
    MATCH (lb:LoadBalancerV2)-[:ELBV2_LISTENER]->(l:ELBV2Listener)
    WHERE lb.scheme = "internet-facing"
    RETURN DISTINCT lb.dnsname as dnsname, l.port as port
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


## What roles have permissions to ECS
```cypher
   match (r:AWSRole)--(pol:AWSPolicy)--(stmt:AWSPolicyStatement) where any(x in stmt.action where x contains 'ecs') return * limit 30;
```

## List all users with too much access to any given resource
```cypher
MATCH(user:AWSUser)--(policy:AWSPolicy)--(statement:AWSPolicyStatement{resource:['*']})
RETURN *
```

## List all S3 buckets and their S3ACLs
```cypher
    MATCH (s:S3Bucket)-[to]-(a:S3Acl) return a,to,s
```

## What S3 buckets have a policy granting anonymous access
```cypher
   MATCH (s:S3Bucket) where s.anonymous_access = true return s
```
