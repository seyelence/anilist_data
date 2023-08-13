import time
from fetch_data import fetch_all_anime_data
from write_csv import write_anime_csv
from database import create_anime_info_table, insert_data_to_anime_info_table
from sqlalchemy import MetaData, create_engine

def main():
    all_anime_details = fetch_all_anime_data()
    csv_file = 'anime_data.csv'
    write_anime_csv(all_anime_details, csv_file)

    connection_string = 'mssql+pyodbc://@THAMANYS-DESKTO/Anime_Collection?trusted_connection=yes&driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes'
    engine = create_engine(connection_string, fast_executemany=True)
    create_anime_info_table(engine, if_exists='replace')
    insert_data_to_anime_info_table(engine, csv_file)

if __name__ == '__main__':
    main()