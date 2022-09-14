"""
League of Legends Hours/Games estimate based on Mastery Points

Programmed by: Selina Ding
https://github.com/SelinaD23

"""

import requests

SUMMONER_LOOKUP_API = ".api.riotgames.com/lol/summoner/v4/summoners/by-name/"
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


def obtain_user_information():
    """
    Prompts the user to input their region and API key

    :return: User's region and API key
    """
    print("Welcome to the No Life Calculator")
    print("==========================================")

    region_menu = "REGION MENU\n" \
                  "==============================\n" \
                  "North America................1\n" \
                  "Europe Nordic & East.........2\n" \
                  "Europe West..................3\n" \
                  "Oceania......................4\n" \
                  "Korea........................5\n" \
                  "Japan........................6\n" \
                  "Brazil.......................7\n" \
                  "Latin America................8\n" \
                  "Russia.......................9\n" \
                  "Turkey.......................0\n" \
                  "=============================="
    region_selection = ""
    print(region_menu)
    while not region_selection.isdigit() or len(region_selection) != 1:
        region_selection = input("Please input the digit corresponding to your region: ")
        if not region_selection.isdigit() or len(region_selection) != 1:
            print("Selection Error. Please try again")
        elif region_selection == "8":
            region_selection += "0"
            latin_input = ""
            while latin_input != "north" or latin_input != "south":
                print("Are you in Latin America North or Latin America South?")
                latin_input = input("Please input North or South ").lower()
            if latin_input == "south":
                region_selection = "81"

    print()
    api_key = input("Please input your API key: ")
    return api_key, region_selection


def generate_profile(api_key):
    """
    Generates new profiles on loop

    :param api_key: str - User's API Key
    :return: None
    """
    encrypted_summoner_id = 404
    while encrypted_summoner_id == 404:
        encrypted_summoner_id = obtain_summoner_id(api_key)
        if type(encrypted_summoner_id) == str:
            print(encrypted_summoner_id)
            if input("Would you like to exit [Yes/No]? ").lower() in "no":
                encrypted_summoner_id = 404
        else:
            print(STATUS_CODE[encrypted_summoner_id])


def obtain_summoner_id(api_key):
    """
    Asks the user to input their Summoner ID and returns the encrypted string upon success

    :param api_key: str - User's API Key
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
    api_key, region_selection = obtain_user_information()
    generate_profile(api_key)

    print("==========================================")
    print("Shutting off...")


main()
