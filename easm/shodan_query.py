import shodan
import os
import csv
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Shodan Search and Export Script')
parser.add_argument('-k', '--keyword', help='Keyword to search for in Shodan')
parser.add_argument('-o', '--output', help='Filename for the CSV output')
parser.add_argument('-cn', '--commonname', help='Common Name (e.g. Domain Name) to search in SSL certificates')
args = parser.parse_args()

# Load the API key from an environment variable
SHODAN_API_KEY = os.getenv('SHODAN_API_KEY')
if not SHODAN_API_KEY:
    raise Exception('SHODAN_API_KEY environment variable not set')

# Initialize the Shodan client
api = shodan.Shodan(SHODAN_API_KEY)

try:
    search_query = ''
    if args.keyword:
        search_query = args.keyword
    if args.commonname:
        search_query = f" ssl.cert.subject.CN:{args.commonname}"
    if not search_query:
        raise Exception('You must provide a keyword or common name to search for')

    # Open a CSV file to write the results
    with open(args.output, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['IP', 'Hostnames', 'Domains', 'Country', 'Open Ports', 'Discovered Services', 'Tags', 'Cloud', 'Data', 'Vulnerabilities'])

        loaded_results = 0
        page = 1
        total_results = 1  # Initialize to enter the loop

        while loaded_results < total_results:
            # Perform the search on Shodan
            results = api.search(search_query, page=page)
            total_results = results['total']
            print(f'Found {total_results} results. Loading page {page}')
            # Loop through the results
            for result in results['matches']:
                ip = result['ip_str']
                hostnames = result.get('hostnames', [])
                domains = ', '.join(hostnames)
                country = result.get('location', {}).get('country_name', 'N/A')
                open_ports = result.get('port', '')
                services = result.get('product', '')
                tags = ', '.join(result.get('tags', []))
                cloud = result.get('cloud', {}).get('provider', 'N/A')
                data = result.get('data', '').replace('\n', ' ')
                vulns = result.get('vulns', {})
                vulns = ', '.join(vulns.keys())
                # Write the result to the CSV file
                writer.writerow([ip, hostnames, domains, country, open_ports, services, tags, cloud, data, vulns])
                loaded_results += 1
                if loaded_results % 10 == 0:
                    print(f'Loaded {loaded_results} results so far')
            if total_results < 100 or loaded_results == total_results:
                break
            page += 1

    print(f'Successfully wrote results {loaded_results} to {args.output}')

except shodan.APIError as e:
    print(f'Error: {e}')
