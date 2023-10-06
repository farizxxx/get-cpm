import requests
import json
import csv
from datetime import datetime, timedelta

# Define the URL with placeholders for the current date
url = "https://api3.adsterratools.com/publisher/5065dc0eecd8d7adee64b9094adc50d0/stats.json?start_date={}&finish_date={}&group_by=date"

# Calculate the current date in UTC
current_utc_date = (datetime.utcnow() + timedelta(hours=7)).strftime("%Y-%m-%d")

# Format the URL with the current date
url = url.format(current_utc_date, current_utc_date)

# Send an HTTP GET request to fetch the JSON data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = json.loads(response.text)
    
    # Extract relevant data
    items = data.get("items", [])
    
    if items:
        item = items[0]  # Assuming there is only one item in the list
        db_date_time_utc = datetime.strptime(data["dbDateTime"], "%Y-%m-%d %H:%M:%S")
        db_date_utc = db_date_time_utc.strftime("%Y-%m-%d")
        db_time_utc = db_date_time_utc.strftime("%H:%M:%S")
        
        cpm = item["cpm"]
        
        # Convert UTC date and time to local time (UTC+7)
        db_date_local = (db_date_time_utc + timedelta(hours=7)).strftime("%Y-%m-%d")
        db_time_local = (db_date_time_utc + timedelta(hours=7)).strftime("%H:%M:%S")
        
        # Append the data to the CSV file
        with open("output.csv", "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([db_date_utc, db_time_utc, db_date_local, db_time_local, cpm])
        
        print("Data has been scraped and appended to output.csv.")
    else:
        print("No data found in the JSON response.")
else:
    print("Failed to fetch data. Status code:", response.status_code)
