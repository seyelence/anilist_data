import time
import requests

API_ENDPOINT = 'https://graphql.anilist.co'
PER_PAGE = 50

# GraphQL query
query = '''
# Define which variables will be used in the query (page, per page)
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
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

def fetch_all_anime_data():
  all_anime_details = []
  page = 1
    
  while len(all_anime_details) <= 15000:
    response = fetch_anime_data(page)
    anime_list = response['data']['Page']['media']
    all_anime_details += anime_list
    if not response['data']['Page']['pageInfo']['hasNextPage']:
      break
      
    page += 1
    time.sleep(60)

  return all_anime_details

all_data = fetch_all_anime_data()
print("Fetched total entries:", len(all_data))