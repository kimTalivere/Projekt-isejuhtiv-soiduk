import psycopg2
import pandas as pd

# Database connection parameters
db_params = {
    'dbname': 'auto',  # replace with your database name
    'user': 'postgres',          # replace with your username
    'password': 'password',      # replace with your password
    'host': 'localhost',              # or your host
    'port': '5432'                    # or your port
}

def fetch_data():
    # Establish a database connection
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Fetch all tables in the database
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = cursor.fetchall()

    all_data = {}

    # Retrieve data from each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM {table_name};")
        records = cursor.fetchall()
        
        # Get column names
        col_names = [desc[0] for desc in cursor.description]
        
        # Store data in a DataFrame for better readability
        df = pd.DataFrame(records, columns=col_names)
        all_data[table_name] = df

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return all_data

if __name__ == "__main__":
    data = fetch_data()
    for table, df in data.items():
        print(f"Data from table: {table}")
        print(df)