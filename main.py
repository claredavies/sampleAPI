import json
import requests

# Constants for error messages
HTTP_ERROR_MSG = "HTTP error: {}"
NETWORK_ERROR_MSG = "Network error: {}"
JSON_PARSE_ERROR_MSG = "JSON parsing error: {}"
UNEXPECTED_ERROR_MSG = "An unexpected error occurred: {}"

# Define the URL for the GET and POST APIs
API_URL = 'https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=0abf770bcf0a391d636e10e45351'


class Partner:
    def __init__(self, firstName, lastName, email, country, availableDates):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.country = country
        self.availableDates = availableDates


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


def main():
    # Check if the GET request was successful (status code 200)
    try:
        get_data = get_response(API_URL)
        if get_data:
            for partner in get_data:
                print(f"Post ID: {partner.firstName}, Title: {partner.lastName}")

        # Define the data for the POST request
        # post_data = {
        #     "userId": 100,
        #     "id": 89,
        #     "title": "Harry Potter",
        #     "body": "Once upon a time"
        # }
        #
        # # Perform the POST request
        # post_response(API_URL, post_data)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
