# External Attack Surface Management - discovering domains
Follow below instructions to perform an external surface scan using public information and subdomains enumeration.

# Querying with Shodan
## Requirements
- [Shodan API](https://developer.shodan.io/api/requirements) key
- Python > 3.10

## Setup
Create e new environment variable to store Shodan API key
```bash
export SHODAN_API_KEY=your_api_key
```

Generate virtual environment
```bash
python3 -m venv ./venv
. ./venv/bin/activate
```

Install shodan python library
```bash
pip install shodan
```

## Run the script to search Shodan by keyword
```bash
 python shodan_query.py -k <ORG_KEYWORD> -o <OUTPUT_CSV_FILE>
```

## Run the script to search Shodan by SSL CN
```bash
  python shodan_query.py -cn <DOMAIN_NAME> -o <OUTPUT_CSV_FILE>
```
# Running EasyEASM
## Requirements
- [Docker](https://docs.docker.com/get-docker/)
- [Slack](https://api.slack.com/messaging/webhooks) and/or [Discord](https://discord.com/developers/docs/resources/webhook) webhooks

## Setup
Copy config_example.yml to a new file named config.yml and fill the data with your own values.

Build the docker image
```bash
cd easyEASM
docker build -t easyasm .
```
## Run the docker image
```bash
docker run easyasm
```
## Check the notfications
Check the notifications sent to configured Slack channel
# Running sub.Monitor (experimental)
## Requirements
- [Docker](https://docs.docker.com/get-docker/)
- Follow [sub.Monitor previous needed configurations](https://github.com/e1abrador/sub.Monitor?tab=readme-ov-file#previous-needed-configurations)

## Setup
Copy `config_examples/` to a new folder named `local_config/` and fill the data with your own values.

Build the docker image
```bash
cd sub.Monitor
docker build -t submonitor .
```
## Run the docker image
```bash
docker run -it submonitor /bin/sh
```

## Follow sub.Monitor instructions
Follow the guidance at https://github.com/e1abrador/sub.Monitor
