import requests
import json

# Step 1: Define the API URL (you can customize this based on your query)
url = "https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_TAX_CIT@DF_CIT_DIVD_INCOME,1.0/.A......?startPeriod=2000&endPeriod=2024"

# Step 2: Define the headers to request JSON format
headers = {
    'Accept': 'application/vnd.sdmx.data+json; charset=utf-8; version=1.0'
}

# Step 3: Send the GET request
response = requests.get(url, headers=headers)

# Step 4: Check the status of the response
if response.status_code == 200:
    # Step 5: Parse the JSON data
    data = response.json()
    
    # Step 6: Save the data as a JSON file
    with open('oecd_div.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print("Data successfully fetched and saved as 'oecd_div.json'.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    print(f"Response content: {response.text[:1000]}")  # Show part of the response if failed
