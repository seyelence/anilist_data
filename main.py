from fetch_data import fetch_all_anime_data
from write_csv import write_anime_csv
from database import create_anime_info_table, insert_data_to_anime_info_table
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

def main():
    target_total_entries = 16000  
    all_anime_details = fetch_all_anime_data(target_total_entries)
    csv_file = 'anime_data.csv'
    write_anime_csv(all_anime_details, csv_file)
    
    load_dotenv()
    db_server = os.getenv('SERVER', default = None)
    db_name = os.getenv('DATABASE', default = None)
    connection_string = f'mssql+pyodbc://@{db_server}/{db_name}?trusted_connection=yes&driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes'
    
    engine = create_engine(connection_string, fast_executemany=True)
    create_anime_info_table(engine, if_exists='replace')
    insert_data_to_anime_info_table(engine, csv_file)

if __name__ == '__main__':
    main()