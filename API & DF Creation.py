import requests
import json
import os
import pandas as pd
# Define URL & Parameters

BASE_URL = "https://data.cms.gov/provider-data/api/1/datastore/query/yv7e-xc69/0"

params = {
    "offset": 1500,
    "count": "true",
    "results": "true",
    "schema": "true",
    "keys": "true",
    "format": "json",
    "rowIds": "false"
}

# 3. Send the GET request
response = requests.get(BASE_URL, params=params)

# 4. Parse the JSON response
data = response.json()

offset = 0
total = data["count"]
all_list = []
while offset<total:
    params["offset"] = offset
    response = requests.get(BASE_URL, params=params)
    # Raise an exception if the HTTP request returned an error code
    response.raise_for_status()
    data = response.json()
    all_list.extend(data["results"])
    print(f"Offset: {offset}")
    print(f"I have downloaded {len(all_list)}")
    offset+=len(data["results"])

# 5. Convert the list of dictionaries to a DataFrame        
df = pd.DataFrame(all_list)
df.to_csv("cms_hospital_data.csv", index=False)







