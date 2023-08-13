import time
import csv
import requests
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, create_engine
from sqlalchemy import Table, Column, Integer, Float, Date, String, Boolean

API_ENDPOINT = 'https://graphql.anilist.co'
PER_PAGE = 10

# GraphQL query
query = '''
# Define which variables will be used in the query (page, per page)
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    pageInfo {
      total
      currentPage
      lastPage
    }
    media(type: ANIME) {
      id
      title {
        romaji
        english
      }
      description(asHtml: false)
      episodes
      startDate {
              year
              month
              day
            }
      endDate {
        year
        month
        day
      }
      duration
      popularity
      source
      season
      seasonYear
      favourites
      averageScore
      isAdult
      genres
      coverImage {
        large
      }
      studios {
        nodes {
          name
        }
      }
    }
  }
}
'''
anime_info_table = None

def fetch_anime_data(page_num):
  response = requests.post(API_ENDPOINT, json={'query': query, 'variables': {'page': page_num, 'perPage': PER_PAGE}})
  return response.json()

def write_anime_csv(data, file_name):
  with open(file_name, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Anime ID', 'Romaji Title', 'English Title', 'Description', 'Episodes', 'Start Date', 'End Date',
      'Duration', 'Popularity', 'Source', 'Season', 'Year', 'Favorites', 'Average Score', 'isAdult', 'Genres'])
    for anime in data:
        writer.writerow([
            anime['id'],
            anime['title']['romaji'], anime['title']['english'],
            anime['description'], anime['episodes'],
            anime['startDate'], anime['endDate'],
            anime['duration'], anime['popularity'], anime['source'],
            anime['season'], anime['seasonYear'], anime['favourites'],
            anime['averageScore'], anime['isAdult'],
            ', '.join(anime['genres'])
        ])
  print("Writing to CSV is done")

def create_anime_info_table(engine, if_exists='replace'):
  global anime_info_table
  metadata = MetaData()
  anime_info_table = Table(
    'anime_info', metadata,
    Column('anime_id', Integer, primary_key=True, nullable=False, autoincrement=True),
    Column('romaji_title', String, nullable=True),
    Column('english_title', String, nullable=True),
    Column('description', String, nullable=True),
    Column('episodes', String, nullable=True),
    Column('startDate', String, nullable=True),  
    Column('endDate', String, nullable=True), 
    Column('duration', String, nullable=True),
    Column('popularity', String, nullable=True),
    Column('source', String, nullable=True),
    Column('season', String, nullable=True),
    Column('year', String, nullable=True), 
    Column('favourites', String, nullable=True),
    Column('averageScore', String, nullable=True),
    Column('isAdult', String, nullable=True),
    Column('genres', String, nullable=True),
  )

  if if_exists == 'replace':
    anime_info_table.drop(engine, checkfirst=True)
  metadata.create_all(engine)
  print("Table is created.")


def insert_data_to_anime_info_table(engine, csv_file):
  global anime_info_table 
  df = pd.read_csv(csv_file).fillna('NO VALUE')
  Session = sessionmaker(bind=engine)
  session = Session()

  # insert data from the csv into the database
  for index, row in df.iterrows():
    insert_data = {
    'anime_id': row['Anime ID'],
    'romaji_title': row['Romaji Title'],
    'english_title': row['English Title'],
    'description': row['Description'],
    'episodes': row['Episodes'],
    'startDate': row['Start Date'],
    'endDate': row['End Date'],    
    'duration': row['Duration'],
    'popularity': row['Popularity'],
    'source': row['Source'],
    'season': row['Season'],
    'year': row['Year'],
    'favourites': row['Favorites'],
    'averageScore': row['Average Score'],
    'isAdult': row['isAdult'],
    'genres': row['Genres'],
    }
    session.execute(anime_info_table.insert().values(**insert_data))

  session.commit()
  session.close()
  print("Data has been inserted into the table.")

def main():
  response = fetch_anime_data(1)
  total_anime = response['data']['Page']['pageInfo']['total']
  last_page = response['data']['Page']['pageInfo']['lastPage']
  all_anime_details = []

  for page in range(1, last_page + 1):
    response = fetch_anime_data(page)
    anime_list = response['data']['Page']['media']
    all_anime_details += anime_list
    if page < last_page:
      time.sleep(1)

  csv_file = 'anime_data.csv'
  write_anime_csv(all_anime_details, csv_file)
  connection_string = 'mssql+pyodbc://@THAMANYS-DESKTO/Anime_Collection?trusted_connection=yes&driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes'
  engine = create_engine(connection_string, fast_executemany=True)
  create_anime_info_table(engine, if_exists='replace')
  print("from main")
  insert_data_to_anime_info_table(engine, csv_file)

if __name__ == '__main__':
  main()