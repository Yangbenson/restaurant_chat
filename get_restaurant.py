import requests
import os
import time
import pandas as pd
import threading
from dotenv import load_dotenv

base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
load_dotenv(".env")
api_key = os.environ["GOOGLE_API_KEY"]

def search_places(api_key, query, location, radius):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    all_places = pd.DataFrame()
    params = {
        "query": query,
        "location": location,
        "radius": radius,
        "key": api_key
    }

    for _ in range(1):

        response = requests.get(base_url, params=params)
        results = response.json()

        all_places = pd.concat([all_places, pd.DataFrame(results['results'])], ignore_index=True)

        if 'next_page_token' not in results:
            break  # Break the loop if no next page token is present

        params['pagetoken'] = results['next_page_token']
        time.sleep(3)  # Sleep to ensure the token is valid for the next request

    return all_places


def get_place_details(place_id, api_key):

    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        # "fields": "name,price_level,rating,reviews",  # fields裡面不能加空格
        "key": api_key,
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
    restaurant_info = pd.DataFrame(columns=['name',
                                            'place_id',
                                            'price_level',
                                            'rating',
                                            'formatted_address',
                                            'dine_in',
                                            'serves_beer',
                                            'serves_breakfast',
                                            'serves_brunch',
                                            'serves_dinner',
                                            'serves_lunch',
                                            'serves_vegetarian_food',
                                            'serves_wine',
                                            'reviews'
                                            ])
    for index, row in places[['name', 'place_id']].iterrows():

        name = row['name']
        place_id = row['place_id']

        place_details = get_place_details(place_id, api_key)
        if place_details:

            print(f"Index: {index}")

            price_level = place_details['result'].get('price_level', None)
            rating = place_details['result'].get('rating', None)
            formatted_address = place_details['result'].get('formatted_address', None)
            dine_in = place_details['result'].get('dine_in', None)
            serves_beer = place_details['result'].get('serves_beer', None)
            serves_breakfast = place_details['result'].get('serves_breakfast', None)
            serves_brunch = place_details['result'].get('serves_brunch', None)
            serves_dinner = place_details['result'].get('serves_dinner', None)
            serves_lunch = place_details['result'].get('serves_lunch', None)
            serves_vegetarian_food = place_details['result'].get('serves_vegetarian_food', None)
            serves_wine = place_details['result'].get('serves_wine', None)

            reviews = '\n'.join(
                f"rating : {review.get('rating', None)}, review : {review.get('text', None)}"
                for review in place_details['result']["reviews"][:3]
                # for review in place_details['result']["reviews"][:3]
            )

            # review = []
            # for i in place_details['result']["reviews"][:3]:
            #     review.append(f"rating : {i.get('rating', None)}, review : {i.get('text', None)}")
            # reviews = '\n'.join(review)

            # 放進dataframe裡
            restaurant_info.loc[index] = [name,
                                          place_id,
                                          price_level,
                                          rating,
                                          formatted_address,
                                          dine_in,
                                          serves_beer,
                                          serves_breakfast,
                                          serves_brunch,
                                          serves_dinner,
                                          serves_lunch,
                                          serves_vegetarian_food,
                                          serves_wine,
                                          reviews]

        else:
            print("No data available.")

    return restaurant_info

""" ----------------------------- Start ---------------------------------- """

def search(query,location):

    restaurants = get_restaurant_info(api_key,query,location,50)
    restaurants['gpt_prompt'] = restaurants.apply(lambda row: f"Name: {row['name']}, "
                                            f"Price Level: {row['price_level']}, "
                                            f"Rating: {row['rating']}, "
                                            f"Address: {row['formatted_address']}, "
                                            f"Dine In: {'Yes' if row['dine_in'] else 'No'}, "
                                            f"Serves Beer: {'Yes' if row['serves_beer'] else 'No'}, "
                                            f"Serves Breakfast: {'Yes' if row['serves_breakfast'] else 'No'}, "
                                            f"Serves Brunch: {'Yes' if row['serves_brunch'] else 'No'}, "
                                            f"Serves Dinner: {'Yes' if row['serves_dinner'] else 'No'}, "
                                            f"Serves Lunch: {'Yes' if row['serves_lunch'] else 'No'}, "
                                            f"Serves Vegetarian Food: {'Yes' if row['serves_vegetarian_food'] else 'No'}, "
                                            f"Serves Wine: {'Yes' if row['serves_wine'] else 'No'}, "
                                            f"Reviews: {row['reviews']}" if row['reviews'] else "No reviews available.",
                                axis=1)

    return restaurants