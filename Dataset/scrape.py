import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Function to get webpage content
def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve content from {url}")
        return None
# Function to convert height in feet/inches to centimeters
def height_to_cm(height_str):
    # Example: '5\'8"' to (5*30.48) + (8*2.54) cm
    match = re.match(r'(\d+)\'(\d+)" \((\d+) cm\)', height_str)
    if match:
        return int(match.group(3))  # Return the value inside the parentheses
    return None

# Function to convert weight in lbs to kilograms
def weight_to_kg(weight_str):
    # Example: '126 lbs (57 kg)'
    match = re.match(r'(\d+) lbs \((\d+) kg\)', weight_str)
    if match:
        return int(match.group(2))  # Return the value inside the parentheses
    return None

# Function to extract the required celebrity details
def extract_celebrity_details(content):
    soup = BeautifulSoup(content, 'html.parser')

    # Extract celebrity name from the <h1> tag
    name = soup.find('h1').text.strip()

    # Extract body measurements table
    table = soup.find('table', class_='bodyMeasurements')
    
    # Initialize the dictionary with name
    details = {'Name': name}

    # Extract the specific fields we need from the table
    for row in table.find_all('tr'):
        key = row.find('td').text.strip()  # Key
        value = row.find_all('td')[1].text.strip()  # Value

        if key == 'Body Shape':
            details['Body Shape'] = value
        elif key == 'Height':
            details['Height'] = height_to_cm(value)
        elif key == 'Weight':
            details['Weight'] = weight_to_kg(value)
        elif key == 'Shoe Size':
            details['Shoe Size'] = value

    return details

# Function to read URLs from a text file
def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
        return [url.strip() for url in urls]  # Strip newlines and spaces

# Main function to scrape all URLs from the file
def scrape_from_url_list(file_path):
    # Read the URLs from the file
    urls = read_urls_from_file(file_path)
    
    all_celebrity_data = []
    
    # Visit each URL and extract details
    for url in urls:
        celebrity_page = get_page_content(url)
        if celebrity_page:
            celebrity_data = extract_celebrity_details(celebrity_page)
            all_celebrity_data.append(celebrity_data)
    
            print(celebrity_data)
    # Create a DataFrame and save as CSV
    df = pd.DataFrame(all_celebrity_data)
    df.to_csv('celebrity_body_measurements.csv', index=False)
    print("Scraping complete. Data saved to celebrity_body_measurements.csv")

# Usage Example: Provide the path to your text file containing URLs
file_path = 'celebURLS.txt'
scrape_from_url_list(file_path)


# u = "https://bodymeasurements.org/en/rihanna/"
# print(get_page_content(u))