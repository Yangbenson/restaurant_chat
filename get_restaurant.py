import requests
import os
import time
import pandas as pd

base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

def search_places(api_key, query, location, radius):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    all_places = pd.DataFrame()
    params = {
        "query": query,
        "location": location,
        "radius": radius,
        "key": api_key
    }

    while True:
        response = requests.get(base_url, params=params)
        results = response.json()

        all_places = pd.concat([all_places, pd.DataFrame(results['results'])], ignore_index=True)

        if 'next_page_token' in results:
            params['pagetoken'] = results['next_page_token']
            time.sleep(3)# 給他時間讀
        else:
            break

    return all_places


def get_place_details(place_id, api_key):

    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,price_level,rating,reviews",  # fields裡面不能加空格
        "key": api_key
    }

    response = requests.get(base_url, params=params)
    place_details = response.json()

    if response.status_code == 200:
        return place_details
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
        return {}

def get_restaurant_info(api_key,query,location,raidus):

    places = search_places(api_key, query, location, raidus)

    ### 抓店家資料
    restaurant_info = pd.DataFrame(columns=['name', 'place_id', 'price_level', 'rating', 'reviews'])
    for index, row in places[['name', 'place_id']].iterrows():

        name = row['name']
        place_id = row['place_id']

        place_details = get_place_details(place_id, api_key)
        if place_details:
            print(f"Index: {index}")
            # print(place_details['result'])
            price_level = place_details['result'].get('price_level', None)
            rating = place_details['result'].get('rating', None)
            reviews = place_details['result'].get('reviews', None)

            # 放進dataframe裡
            restaurant_info.loc[index] = [name, place_id, price_level, rating, reviews]

        else:
            print("No data available.")

    return restaurant_info

def get_location():
    # 使用免费或付费的 IP 定位服务
    response = requests.get('http://ipinfo.io/json')
    data = response.json()
    return data['loc']  # 'loc' 包含了经纬度信息

""" ----------------------------- Start ---------------------------------- """

# api_key = os.environ["GOOGLE_API_KEY"]
query = "Japanese Restaurant"
location = "40.712776,-74.005974"  # Latitude and longitude of New York City

# restaurants = get_restaurant_info(api_key,query,location,500)
#
# print(get_location())