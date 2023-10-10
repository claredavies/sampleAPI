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
API__GET_URL = 'https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=0abf770bcf0a391d636e10e45351'
API_POST_URL = 'https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=0abf770bcf0a391d636e10e45351'

sample_data = {
    "partners": [
        {
            "firstName": "Darin",
            "lastName": "Daignault",
            "email": "ddaignault@hubspotpartners.com",
            "country": "United States",
            "availableDates": [
                "2017-05-03",
                "2017-05-06"
            ]
        },
        {
            "firstName": "Crystal",
            "lastName": "Brenna",
            "email": "cbrenna@hubspotpartners.com",
            "country": "Ireland",
            "availableDates": [
                "2017-04-27",
                "2017-04-29",
                "2017-04-30"
            ]
        },
        {
            "firstName": "Janyce",
            "lastName": "Gustison",
            "email": "jgustison@hubspotpartners.com",
            "country": "Spain",
            "availableDates": [
                "2017-04-29",
                "2017-04-30",
                "2017-05-01"
            ]
        },
        {
            "firstName": "Tifany",
            "lastName": "Mozie",
            "email": "tmozie@hubspotpartners.com",
            "country": "Spain",
            "availableDates": [
                "2017-04-28",
                "2017-04-29",
                "2017-05-01",
                "2017-05-04"
            ]
        },
        {
            "firstName": "Temple",
            "lastName": "Affelt",
            "email": "taffelt@hubspotpartners.com",
            "country": "Spain",
            "availableDates": [
                "2017-04-28",
                "2017-04-29",
                "2017-05-02",
                "2017-05-04"
            ]
        },
        {
            "firstName": "Robyn",
            "lastName": "Yarwood",
            "email": "ryarwood@hubspotpartners.com",
            "country": "Spain",
            "availableDates": [
                "2017-04-29",
                "2017-04-30",
                "2017-05-02",
                "2017-05-03"
            ]
        },
        {
            "firstName": "Shirlene",
            "lastName": "Filipponi",
            "email": "sfilipponi@hubspotpartners.com",
            "country": "Spain",
            "availableDates": [
                "2017-04-30",
                "2017-05-01"
            ]
        },
        {
            "firstName": "Oliver",
            "lastName": "Majica",
            "email": "omajica@hubspotpartners.com",
            "country": "Spain",
            "availableDates": [
                "2017-04-28",
                "2017-04-29",
                "2017-05-01",
                "2017-05-03"
            ]
        },
        {
            "firstName": "Wilber",
            "lastName": "Zartman",
            "email": "wzartman@hubspotpartners.com",
            "country": "Spain",
            "availableDates": [
                "2017-04-29",
                "2017-04-30",
                "2017-05-02",
                "2017-05-03"
            ]
        },
        {
            "firstName": "Eugena",
            "lastName": "Auther",
            "email": "eauther@hubspotpartners.com",
            "country": "United States",
            "availableDates": [
                "2017-05-04",
                "2017-05-09"
            ]
        }
    ]
}


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


def get_response_sample_data():
    json_data = sample_data
    post_objects = [Partner(**item) for item in json_data["partners"]]
    return post_objects


def get_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
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
    try:
        response = requests.post(url, json=data)

        # Check if the POST request was successful
        if response.status_code == 201:
            print("POST request successful!")
        else:
            print(f"POST request failed with status code {response.status_code}")

    except requests.exceptions.HTTPError as e:
        raise Exception(HTTP_ERROR_MSG.format(e))
    except requests.exceptions.RequestException as e:
        raise Exception(NETWORK_ERROR_MSG.format(e))
    except Exception as e:
        raise Exception(UNEXPECTED_ERROR_MSG.format(e))


def separate_countries(partner_list):
    country_map = {}
    print(type(partner_list))

    # Iterate through the list of Partner objects and group them by country
    for partner in partner_list:
        print(partner)
        country = partner.country  # Access the 'country' attribute
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
    print("Ans:", earliest_date)
    return earliest_date


def get_date_counts(partner_list):
    date_counts = {}
    for partner in partner_list:
        available_dates = partner.availableDates
        for available_date in available_dates:
            if available_date not in date_counts:
                date_counts[available_date] = 1
            else:
                date_counts[available_date] += 1
    return date_counts


def get_partners_email_match_dates(partners, wanted_date):
    partners_email_with_optimal_date = []

    for partner in partners:
        available_dates = partner.availableDates
        for date in available_dates:
            if datetime.strptime(date, "%Y-%m-%d").date() == wanted_date:
                partners_email_with_optimal_date.append(partner.email)
    partners_email_with_optimal_date.sort()
    return partners_email_with_optimal_date


def main():
    # Check if the GET request was successful (status code 200)
    try:
        # partner_list = get_response(API__GET_URL)
        partner_list = get_response_sample_data()

        country_map = separate_countries(partner_list)
        attendance_list = []
        for country, partner_list_country in country_map.items():
            optimal_date_country = find_optimal_date_for_country(partner_list_country)
            print(f"country: {country}, optimal_date_country: {optimal_date_country}")
            if optimal_date_country is not None:
                partner_email_match = get_partners_email_match_dates(partner_list_country, optimal_date_country)
                num_people = len(partner_email_match)
                attendance_list.append(Attendance(num_people, partner_email_match, country, optimal_date_country.strftime("%Y-%m-%d")))
            else:
                attendance_list.append(Attendance(0, [], country, None))

        data = {"countries": [vars(attendance) for attendance in attendance_list]}
        json_data = json.dumps(data, indent=2)
        print(json_data)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
