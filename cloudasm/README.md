# Cloud Attack Surface Management - Assets Discovery

# CloudQuery AWS Assets Discovery and Visualization

## Requirements
- AWS Account
- AWS authentication credentials (see [CloudQquery -> plugins -> AWS -> Authentication](https://hub.cloudquery.io/plugins/source/cloudquery/aws/latest/docs#authentication) )
- [Docker compose](https://docs.docker.com/compose/)
- [CloudQuery account](https://www.cloudquery.io/auth/register)

## Setup 
[Generate a CloudQuery API key](https://docs.cloudquery.io/docs/deployment/generate-api-key)

Create a `.env` file at [cloudquery](./cloudquery) with content: `CLOUDQUERY_API_KEY=your_api_key`

Setup AWS credentials either at `.env` or at `~/.aws/credentials`
```bash
AWS_ACCESS_KEY_ID={Your AWS Access Key ID}
AWS_SECRET_ACCESS_KEY={Your AWS secret access key}
```

Sample `.env`:
```bash
CLOUDQUERY_API_KEY=your_api_key
AWS_ACCESS_KEY_ID={Your AWS Access Key ID}
AWS_SECRET_ACCESS_KEY={Your AWS secret access key}
```

## Build containers with docker compose
Go to [/cloudquery](./cloudquery) and run docker compose up
```bash
cd ./cloudquery
docker-compose up -d
```

## Run CloudQuery sync
```bash
docker-compose run cloudquery
```
It can take around 15-25 minutes to complete, so be patient.

## See results in grafana
Follow the instructions from [cloudquery/plugins/source/aws/dashboards#aws-asset-inventory](https://github.com/cloudquery/cloudquery/tree/main/plugins/source/aws/dashboards#aws-asset-inventory)

Open Grafana for the first time at http://localhost:3000 and [sign in](https://grafana.com/docs/grafana/latest/setup-grafana/sign-in-to-grafana/) using `admin/admin` credentials.

Open a shell into the postgres DB and run the resources.sql script
```bash
docker exec -it cloudquery-postgres-1 bash
psql -U postgres < /var/lib/postgresql/scripts/resources.sql
```

Add the CloudQuery postgres database as a data source to Grafana (Connections -> Data Sources -> Add new data source)
- Set the host url to `postgres:5432`
- Set credentials postgres/pass
- Disable TLS/SSL Mode
- Save and test connection

Import the dashboards from [cloudquery/grafana](./cloudquery/grafana/)

Play around with more queries from CloudQuery [query examples](https://hub.cloudquery.io/plugins/source/cloudquery/aws/latest/docs#query-examples) or the formerly Cloud Security Posture Management (CSPM) [policies queries](https://github.com/cloudquery/cloudquery/tree/main/plugins/source/aws/policies_v1). 

## Alternative path dbt (experimental)
Follow instructions from OpenSource CSPM [how to guide](https://docs.cloudquery.io/how-to-guides/open-source-cspm).

Install dbt from their [Docker image](https://docs.getdbt.com/docs/core/docker-install).

Add the dbt container to `docker-compose.yml` file.

# Cartography AWS Assets Discovery and Visualization

## Setup
- AWS Account
- AWS authentication credentials ([follow single AWS account setup](https://lyft.github.io/cartography/modules/aws/config.html), at least adding the [SecurityAudit policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions.html#jf_security-auditor) to your AWS connected credentials)
- [Docker compose](https://docs.docker.com/compose/)

## Option 1 - clone cartography and build locally
Used a slightly different [Dockerfile](./cartography/Dockerfile) from the [official one](https://github.com/lyft/cartography/blob/master/Dockerfile), hence you have to build it locally.

Clone locally Cartography GitHub repository
```bash
cd cartography
git clone https://github.com/lyft/cartography.git
docker build -t lyft/cartography .
```

## Option 2 - use predefined build
Update the [docker-compose-yml](./cartography/docker-compose.yml) file to point out to [heryxpc/cartography](https://hub.docker.com/repository/docker/heryxpc/cartography/general)
```yaml
  cartography:
    image: heryxpc/cartography
    user: cartography
    init: true
```

## Build containers with Docker compose
```bash
docker-compose up -d
```

## Run Cartography sync
```bash
docker-compose run cartography cartography --neo4j-uri bolt://neo4j:7687
```
Takes around 45 minutes to complete.

## Visualize data with NeoDash
1. Open NeoDash at http://localhost:5005/
1. Click on New Dashboard
1. Use defaults and set `localhost` as `Hostname``
1. Click the _load_ button from the left panel (small cloud with up arrow)
1. Choose _Select From File_
1. Open the file [neodash/dashboard.json](./neodash/dashboard.json)
1. Click on _Load Dashboard_
1. Play around with the information presented

## Option 3 - use neo4j dump backup
Would need to `restart` and `healthcheck`options from the [docker-compose.yaml](./cartography/docker-compose.yaml) to avoid Docker to keep restarting neo4j when shutting down.
```yml
# restart: unless-stopped
# healthcheck:
#         test: ["CMD", "curl", "-f", "http://localhost:7474"]
#         interval: 10s
#         timeout: 10s
#         retries: 10
```

Open a terminal at the neo4j container and stop neo4j
```bash
docker exec -it cartography-neo4j-1 bash
neo4j stop
```

Copy the DB dump from [sample_data](./cartography/sample_data) folder to the container
```bash
docker cp ./cartography/sample_data/neo4j.dump cartography-neo4j-1:/import/neo4j.dump
```

From the container, run the backup restore command and restart neo4j
```bash
neo4j-admin load --from=/var/lib/neo4j/import --database=neo4j --force
neo4j start
```
