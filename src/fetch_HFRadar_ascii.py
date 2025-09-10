import os
import requests
from bs4 import BeautifulSoup
import wget


#pip install requests beautifulsoup4 wget

url = input('Enter the web address of where the HFRadar file are located: ')
# e.g  "https://www.ncei.noaa.gov/data/oceans/ndbc/hfradar/radial/2023/202306/Rutgers/MVCO/"

# Send an HTTP GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the anchor tags (links) in the webpage
    links = soup.find_all('a')
    
    # Filter the links to get only those starting with 'RDL_' and limit to the first 10
    rdl_links = [link.get('href') for link in links if link.get('href').startswith('RDL_')][:10]
    
    # Specify the directory where you want to save the downloaded files
    download_directory = "data/hfradar_ascii/"
    
    # Create the directory if it doesn't exist
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    
    # Download the files
    for rdl_link in rdl_links:
        file_url = url + rdl_link
        file_name = os.path.join(download_directory, rdl_link)
        
        # Download the file using wget
        wget.download(file_url, out=file_name)
        
    print("Download completed.")
else:
    print("Failed to retrieve the webpage.")

