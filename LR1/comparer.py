import time
from difflib import SequenceMatcher

def measure_response_time(api_function, *args, **kwargs):
    """
    Measures the response time of a given API function.

    :param api_function: The API function to measure.
    :param args: Positional arguments for the API function.
    :param kwargs: Keyword arguments for the API function.
    :return: Tuple containing the response and the time taken (in seconds).
    """
    start_time = time.time()
    response = api_function(*args, **kwargs)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return response, elapsed_time

def calculate_content_similarity(content1: str, content2: str) -> float:
    """
    Calculates the similarity ratio between two pieces of content.

    :param content1: First content string.
    :param content2: Second content string.
    :return: Similarity ratio as a percentage.
    """
    similarity_ratio = SequenceMatcher(None, content1, content2).ratio()
    return similarity_ratio * 100

def compare_results(result1: str, result2: str, time1: float, time2: float) -> str:
    """
    Compares the results from two APIs, including response time, content length, and similarity.

    :param result1: The result from the first API.
    :param result2: The result from the second API.
    :param time1: The response time of the first API (in seconds).
    :param time2: The response time of the second API (in seconds).
    :return: A comparison summary string.
    """
    length1 = len(result1)
    length2 = len(result2)
    similarity = calculate_content_similarity(result1, result2)

    comparison = (
        f"Speed: Free Dictionary ({time1:.2f} seconds) vs Merriam-Webster ({time2:.2f} seconds)\n"
        f"Length: Free Dictionary ({length1} chars) vs Merriam-Webster ({length2} chars)\n"
        f"Content similarity: {similarity:.2f}%"
    )
    return comparison
