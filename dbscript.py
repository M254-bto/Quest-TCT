import pandas as pd
import requests

# Function to clean the CSV and post data to the Django backend
def clean_and_post_csv(csv_file, api_endpoint):
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)

        # Replace missing values
        

         #Ensure no NaN values remain in the DataFrame
        df = df.fillna('')  # Fallback to empty strings if any NaN persists

        # Post each row to the Django backend
        for _, row in df.iterrows():
            child_data = row.to_dict()  # Convert row to a dictionary
            response = requests.post(api_endpoint, json=child_data)
            if response.status_code == 201:  # 201 Created
                print(f"Successfully created: {child_data['name']}")
            else:
                print(f"Failed to create: {response.json()}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Main script
if __name__ == "__main__":
    # Replace with your CSV file path and Django API endpoint
    csv_file_path = 'Docs/visitors.csv'
    api_endpoint_url = 'http://localhost:8000/'  # Replace with your actual API endpoint

    clean_and_post_csv(csv_file_path, api_endpoint_url)
