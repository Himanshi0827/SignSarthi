import requests
from bs4 import BeautifulSoup
import re

# Step 1: Scrape the main page to get the file names
main_url = 'https://zenodo.org/records/4010759'
response = requests.get(main_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all file links
file_links = []
for td in soup.find_all('td', class_='ten wide'):
    link_tag = td.find('a')
    if link_tag and 'download=1' in link_tag['href']:
        file_links.append(link_tag.text.strip())

# Step 2: For each file, go to the preview page and extract relevant data
preview_url_template = 'https://zenodo.org/records/4010759/preview/{}?include_deleted=0'

# For each file, construct the preview URL and scrape the data
for file_name in file_links:
    preview_url = preview_url_template.format(file_name)
    response = requests.get(preview_url)
    preview_soup = BeautifulSoup(response.text, 'html.parser')
    
    tree_items = preview_soup.find_all('a', href=re.compile(r'#tree_item\d+'))
    for item in tree_items:
        section_name = item.text.strip()
        print(f'Found section "{section_name}" in {file_name}')