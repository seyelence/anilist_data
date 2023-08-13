import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, create_engine, Table, Column, Integer, String, Boolean

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
