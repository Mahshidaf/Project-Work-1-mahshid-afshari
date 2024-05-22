import requests
import pandas as pd
import sqlite3
import os

# Function to download and save the CSV
def download_csv(url, save_path):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded CSV to {save_path}")

# Function to transform and clean the data
def transform_data(csv_path):
    try:
        df = pd.read_csv(csv_path)
        # Perform any transformations/cleaning here
        df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]
        return df
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
        return None

# Function to save the data to an SQLite database
def save_to_sqlite(df, db_path, table_name):
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"Saved data to SQLite database at {db_path} in table {table_name}")

# Main function to run the pipeline
def main():
    # URLs for the datasets
    url1 = "https://www.eea.europa.eu/data-and-maps/daviz/percentage-of-total-green-infrastructure/download.csv"
    url2 = "https://api.openaq.org/v1/measurements?country=US&limit=10000&format=csv"
    
    # Define file paths
    base_dir = os.getcwd()
    data_dir = os.path.join(base_dir, 'data')
    csv_path1 = os.path.join(data_dir, 'green_infrastructure.csv')
    csv_path2 = os.path.join(data_dir, 'air_quality_data.csv')
    db_path = os.path.join(data_dir, 'combined_data.db')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Download the datasets
    download_csv(url1, csv_path1)
    download_csv(url2, csv_path2)
    
    # Transform the datasets
    df1 = transform_data(csv_path1)
    df2 = transform_data(csv_path2)
    
    if df1 is not None and df2 is not None:
        # Save to SQLite database
        save_to_sqlite(df1, db_path, 'green_infrastructure')
        save_to_sqlite(df2, db_path, 'air_quality')
        print("Data pipeline executed successfully.")
    else:
        print("Data pipeline failed due to CSV parsing errors.")

if __name__ == "__main__":
    main()
