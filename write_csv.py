import csv

def write_anime_csv(data, file_name):
  print("Beginning to write to csv.")
  
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