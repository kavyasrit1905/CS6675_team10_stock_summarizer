import json

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def print_article_lines(data):
    for company in data['companies']:
        print(f"Company: {company['name']} ({company['ticker']})")
        print("Articles:")
        for article in company['articles']:
            print(f"Date: {article['date']}")
            print(f"URL: {article['url']}")
            print("Content:")
            for line in article['content'].split('\n'):
                print(line)
            print()

# Path to your JSON file
json_file_path = 'stock_summary_data.json'

# Read JSON file
data = read_json_file(json_file_path)

# Print article lines
print_article_lines(data)