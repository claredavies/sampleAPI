import json
from collections import Counter
from datetime import datetime, timedelta

import requests

# Constants for error messages
HTTP_ERROR_MSG = "HTTP error: {}"
NETWORK_ERROR_MSG = "Network error: {}"
JSON_PARSE_ERROR_MSG = "JSON parsing error: {}"
UNEXPECTED_ERROR_MSG = "An unexpected error occurred: {}"

# Define the URL for the GET and POST APIs
API_GET_URL = 'https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=0abf770bcf0a391d636e10e45351'
API_POST_URL = 'https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=0abf770bcf0a391d636e10e45351'


class Partner:
    def __init__(self, firstName, lastName, email, country, availableDates):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.country = country
        self.availableDates = availableDates

    def __str__(self):
        return f"Partner(firstName='{self.firstName}', lastName='{self.lastName}', email='{self.email}', country='{self.country}')"


class Attendance:
    def __init__(self, attendeeCount, attendees, name, startDate):
        self.attendeeCount = attendeeCount
        self.attendees = attendees
        self.name = name
        self.startDate = startDate

    def __str__(self):
        return f"Attendance(attendeeCount='{self.attendeeCount}', attendees='{self.attendees}', name='{self.name}', startDate='{self.startDate}')"


def get_response(url):
    try:
        response = requests.get(url)
        json_data = response.json()

        # Create a list of Post objects by deserializing each JSON object
        post_objects = [Partner(**item) for item in json_data["partners"]]
        return post_objects

    except requests.exceptions.HTTPError as e:
        raise Exception(HTTP_ERROR_MSG.format(e))
    except requests.exceptions.RequestException as e:
        raise Exception(NETWORK_ERROR_MSG.format(e))
    except json.JSONDecodeError as e:
        raise Exception(JSON_PARSE_ERROR_MSG.format(e))
    except Exception as e:
        raise Exception(UNEXPECTED_ERROR_MSG.format(e))


def post_response(url, data):
    headers = {'Content-Type': 'application/json'}
    # Send the POST request with the JSON payload
    response = requests.post(url, data=data, headers=headers)

    # Check if the POST request was successful
    if response.status_code == 200:
        print("POST request successful!")
    else:
        print(f"POST request failed with status code {response.status_code}")


def separate_countries(partner_list):
    country_map = {}

    # Iterate through the list of Partner objects and group them by country
    for partner in partner_list:
        country = partner.country
        if country not in country_map:
            country_map[country] = []
        country_map[country].append(partner)
    return country_map


def find_optimal_date_for_country(filtered_data):
    consecutive_dates = []
    for partner in filtered_data:
        available_dates = partner.availableDates
        available_dates = sorted([datetime.strptime(date, "%Y-%m-%d").date() for date in available_dates])

        for i in range(len(available_dates) - 1):
            date1 = available_dates[i]
            date2 = available_dates[i + 1]

            if date2 == date1 + timedelta(days=1):
                consecutive_dates.append(date1)

    if not consecutive_dates:
        return None

    # Count the occurrences of consecutive dates using Counter
    consecutive_date_count = dict(Counter(consecutive_dates))
    max_value = max(consecutive_date_count.values())

    # Find the keys with the maximum value
    max_keys = [key for key, value in consecutive_date_count.items() if value == max_value]
    earliest_date = min(max_keys)
    return earliest_date


def get_partners_email_match_dates(partners, wanted_date):
    partners_email_with_optimal_date = []

    for partner in partners:
        available_dates = partner.availableDates
        for date in available_dates:
            if datetime.strptime(date, "%Y-%m-%d").date() == wanted_date:
                partners_email_with_optimal_date.append(partner.email)
    partners_email_with_optimal_date.sort()
    return partners_email_with_optimal_date


def post_attendance_list():
    try:
        partner_list = get_response(API_GET_URL)
        country_map = separate_countries(partner_list)
        attendance_list = []
        for country, partner_list_country in country_map.items():
            optimal_date_country = find_optimal_date_for_country(partner_list_country)
            if optimal_date_country is not None:
                partner_email_match = get_partners_email_match_dates(partner_list_country, optimal_date_country)
                num_people = len(partner_email_match)
                attendance_list.append(
                    Attendance(num_people, partner_email_match, country, optimal_date_country.strftime("%Y-%m-%d")))
            else:
                attendance_list.append(Attendance(0, [], country, None))

        data = {"countries": [vars(attendance) for attendance in attendance_list]}
        json_data = json.dumps(data, indent=2)
        post_response(API_POST_URL, json_data)

    except Exception as e:
        print(f"Error: {e}")


def main():
    post_attendance_list()


if __name__ == "__main__":
    main()
