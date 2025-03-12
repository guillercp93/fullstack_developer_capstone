import logging
import os

from dotenv import load_dotenv
import requests

load_dotenv()
# Get an instance of a logger
logger = logging.getLogger(__name__)

backend_url = os.getenv("backend_url", default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url", default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    """
    Makes a GET request to the backend API endpoint with optional query parameters.

    Args:
        endpoint (str): The API endpoint to call (e.g., 'fetchReviews', 'fetchDealers')
        **kwargs: Optional keyword arguments that will be converted to URL query parameters
                 Example: dealer_id=123 becomes '?dealer_id=123' in the URL

    Returns:
        dict or None: JSON response from the API if successful, None if request fails

    Example:
        >>> get_request('fetchReviews', dealer_id=123)
        # Makes request to: http://localhost:3030/fetchReviews?dealer_id=123
        # Returns: {'reviews': [...]} or None if failed
    """
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
        # Remove trailing '&' if exists
        params = params.rstrip("&")

    request_url = (
        f"{backend_url}/{endpoint}?{params}" if params else f"{backend_url}/{endpoint}"
    )
    logger.info(f"Request URL: {request_url}")

    try:
        response = requests.get(request_url, timeout=10)  # Add timeout
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON response: {str(e)}")
        return None


def analyze_review_sentiments(text):
    """
    Analyzes the sentiment of a given review text using the sentiment analyzer service.

    Args:
        text (str): The review text to analyze. Should be a string containing the review content.

    Returns:
        dict or None: A dictionary containing sentiment analysis results if successful.
                     Expected format: {'sentiment': 'positive/negative/neutral', 'score': float}
                     Returns None if the request fails or response cannot be parsed.

    Example:
        >>> analyze_review_sentiments("Great service and friendly staff!")
        {'sentiment': 'positive', 'score': 0.8}
        >>> analyze_review_sentiments("Poor experience")
        {'sentiment': 'negative', 'score': -0.6}
    """
    request_url = f"{sentiment_analyzer_url}/analyze/{text}"
    try:
        response = requests.get(request_url, timeout=10)  # Add timeout
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON response: {str(e)}")
        return None


def post_review(endpoint, data_dict):
    """
    Sends a POST request to the specified backend API endpoint with the provided data.

    Args:
        endpoint (str): The API endpoint to which the POST request will be sent.
        data_dict (dict): A dictionary containing the data to be sent in the request body.

    Returns:
        dict or None: A dictionary containing the JSON response from the API if the request is successful.
                      Returns None if the request fails or the response cannot be parsed.

    Example:
        >>> post_review("insert_review", {"name": "John", "review": "Great service!"})
        # Sends a POST request to: http://localhost:3030/insert_review
        # Returns: {'status': 'success', 'id': 1} or None if failed
    """

    request_url = f"{backend_url}/{endpoint}"
    try:
        response = requests.post(request_url, json=data_dict, timeout=10)  # Add timeout
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON response: {str(e)}")
        return None
