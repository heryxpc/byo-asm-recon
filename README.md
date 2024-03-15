# byo-asm-recon
Workshop that shows how to build your own ASM recon on external and cloud assets. Presented at HackGDL 2024 by @heryxpc

## Instructions
You can use any domain or AWS account you are authorized to perform reconnaissance.
I used [CloudGoat](https://github.com/RhinoSecurityLabs/cloudgoat) as it worked smoothly to spin up AWS resources with interesting characteristics, specially when setting the `whitelist.txt` to `0.0.0.0/0`
⚠️ CloudGoat is a vulnerable by design project and spinning it on a production environment puts in risk the AWS account where it's hosted.⚠️


## Demos
Each demo can be executed independently and has it's own requirements. You can check the details for each at:
* [External Attack Surface Management](./easm/README.md)
    * Querying domains with Shodan
    * Running EasyASM to discover new subdomains
    * Running sub.Monitor to discover new subdomains
* [Cloud Security Posture/Cloud Attack Surface](./cloudasm/README.md)
    * Building Cloud Security Dashboards with CloudQuery and Grafana
    * Building Attack Surface Investigation dashboards with Cartography and NeoDash

## References
### Tools
* [EasyASM](https://github.com/g0ldencybersec/EasyEASM) by @g0ldencybersec
* [sub.Monitor](https://github.com/e1abrador/sub.Monitor) by @e1abrador
* [Cartography](https://github.com/lyft/cartography/) by @lyft
* [CloudQuery](https://github.com/cloudquery/cloudquery) by @cloudquery
* [CloudGoat](https://github.com/RhinoSecurityLabs/cloudgoat) by @RhinoSecurityLabs
### Conference talks
* DefCon 31 Recon Village - [Easy EASM The Zero-Dollar Attack Surface Management Tool](https://www.youtube.com/watch?v=hx0dBo-zKE8)
* BSidesSF 2023 - [Container vuln management with (hopefully) minimal burnout](https://www.youtube.com/watch?v=F4EFHK21Et0) by @achantavy
* SASN webcast Offensive Security Operations with [Continuous Attack Surface Management & Always-On Pen Testing](https://www.youtube.com/watch?v=pUwyjjPxrFc) by [@ChrisADale](https://twitter.com/ChrisADale)
* [AWS Asset Inventory dashboard with CQ and Grafana](https://medium.com/opsnetic/aws-asset-inventory-dashboard-with-cloudquery-and-grafana-4d362e8e5a39)
* Official blog post: [How to Build an Open Source CSPM with CloudQuery, PostgreSQL and Grafana](https://docs.cloudquery.io/how-to-guides/open-source-cspm#step-3-install-dbt)
* [CloudQuery Docker deployment](https://docs.cloudquery.io/docs/deployment/docker)
* [CloudQuery AWS plugin tables](https://hub.cloudquery.io/plugins/source/cloudquery/aws/latest/tables)
* [CloudQuery performance tuning](https://docs.cloudquery.io/docs/advanced-topics/performance-tuning)
* [Neo4j in Docker](https://neo4j.com/docs/operations-manual/current/docker/introduction/)
* Cartography [Testing with Docker](https://lyft.github.io/cartography/dev/testing-with-docker.html)
* Engineering at Lyft - [cartography](https://eng.lyft.com/search?q=cartography)

# Acknowledge
Big kudos to @spangenberg and @achantavy for all the help given to prepare this demo 
🙌
