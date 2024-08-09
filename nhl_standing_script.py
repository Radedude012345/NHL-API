import http.client
import json as js
import pandas as pd

# Set up the connection to the API
conn = http.client.HTTPSConnection("v1.hockey.api-sports.io")

# Define the headers with your API key and host
headers = {
    'x-rapidapi-key': 'XxXxXxXxXxXxXxXxXxXxXxXxXx',
    'x-rapidapi-host': 'v1.hockey.api-sports.io'
}

# Iterate over league numbers 1 through 20
for league_id in range(1, 21):
    # Define the API endpoint with parameters for league and season
    endpoint = f"/standings?league={league_id}&season=2019"

    # Make the GET request
    conn.request("GET", endpoint, headers=headers)

    # Get the response from the API
    response = conn.getresponse()

    # Read the response data and decode it
    data = response.read().decode('utf-8')

    # Parse the JSON response
    json_data = js.loads(data)

    # Limit the output to only the relevant data
    filtered_data = {
        "get": json_data.get("get"),
        "parameters": json_data.get("parameters"),
        "errors": json_data.get("errors"),
        "results": json_data.get("results"),
        "response": [
            {
                "position": item["position"],
                "stage": item["stage"],
                "group": item["group"]["name"],
                "team": {
                    "name": item["team"]["name"],
                    "logo": item["team"]["logo"]
                },
                "points": item["points"],
                "form": item["form"],
                "description": item["description"]
            }
            for sublist in json_data.get("response", [])
            for item in sublist
        ]
    }

    # Print the filtered JSON output for the current league
    print(f"Standings for League ID: {league_id}")
    print(js.dumps(filtered_data, indent=4))

    # Optional: convert the response into a Pandas DataFrame for further manipulation
    df = pd.DataFrame(filtered_data["response"])
    print(df)

    # Add a separator for clarity between leagues
    print("\n" + "="*80 + "\n")

# Close the connection after all requests are done
conn.close()
