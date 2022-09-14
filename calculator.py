"""
League of Legends Hours/Games estimate based on Mastery Points

Programmed by: Selina Ding
https://github.com/SelinaD23

"""

import requests
from api_key import api_key

SUMMONER_LOOKUP_API = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
API_KEY_URL = "?api_key="
STATUS_CODE = {400: "Bad request",
               401: "Unauthorized, check your API key",
               403: "Forbidden",
               404: "User not found in NA1. Please try again",
               405: "Method not allowed",
               415: "Unsupported media type",
               429: "Rate limit exceeded",
               500: "Internal server error",
               502: "Bad gateway",
               503: "Service unavailable",
               504: "Gateway timeout"}


def obtain_summoner_id():
    """
    Asks the user to input their Summoner ID and returns the encrypted string upon success

    :return: Encrypted Summoner ID string if successful, Integer value of status code if unsuccessful
    """
    summoner_id = input("Please input your summoner ID: ").lower()
    summoner_lookup = SUMMONER_LOOKUP_API + summoner_id + API_KEY_URL + api_key

    response_api = requests.get(summoner_lookup)

    if response_api.status_code == 200:
        encrypted_summoner_id = response_api.text[len('{"id":"'):response_api.text[7:].find('"')]
        return encrypted_summoner_id

    return response_api.status_code


def main():
    encrypted_summoner_id = 404
    while encrypted_summoner_id == 404:
        encrypted_summoner_id = obtain_summoner_id()
        if type(encrypted_summoner_id) == str:
            print(encrypted_summoner_id)
            encrypted_summoner_id = 404
        else:
            print(STATUS_CODE[encrypted_summoner_id])


main()
