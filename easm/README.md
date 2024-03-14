
# Querying with Shodan
## Setup
Create e new environment varible to store shodan API key
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

# Running sub.Monitor (experimental)
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

# Running EasyEASM
## Setup
Copy config_example.yml to a new file named config.yml and fill the data with your own values.

Build the docker image
```bash
cd EasyEASM
docker build -t easyasm .
```
## Run the docker image
```bash
docker run -v easyasm
```
## Check the notfications
Check the notifications sent to configured Slack channel
