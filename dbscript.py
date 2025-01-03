import pandas as pd
from sqlalchemy import create_engine

# Database connection details
DB_HOST = 'aws-0-us-east-1.pooler.supabase.com'
DB_NAME = 'postgres'
DB_USER = 'postgres.vacehxsjgutxtemyvmti'
DB_PASSWORD = 'NQJ8bVVpwNYDb8dw'
DB_PORT = 6543

# Function to clean and migrate the CSV
def clean_and_migrate_csv(csv_file, table_name):
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)

        # Replace missing values
        for column in df.columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                df[column].fillna(0, inplace=True)
            elif pd.api.types.is_string_dtype(df[column]):
                df[column].fillna('n/a', inplace=True)

        # Connect to the PostgreSQL database
        engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        # Migrate the DataFrame to the PostgreSQL table
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data successfully migrated to the '{table_name}' table in the database.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Main script
if __name__ == "__main__":
    # Replace with your CSV file path and desired PostgreSQL table name
    csv_file_path = 'Docs/quest.csv'
    target_table_name = "attendance_child"

    clean_and_migrate_csv(csv_file_path, target_table_name)
