import time
import requests

API_ENDPOINT = 'https://graphql.anilist.co'
PER_PAGE = 100

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

def fetch_all_anime_data():
    all_anime_details = []
    response = fetch_anime_data(1)
    total_anime = response['data']['Page']['pageInfo']['total']
    last_page = response['data']['Page']['pageInfo']['lastPage']

    for page in range(1, last_page + 1):
        response = fetch_anime_data(page)
        anime_list = response['data']['Page']['media']
        all_anime_details += anime_list
        if page < last_page:
            time.sleep(1)

    return all_anime_details