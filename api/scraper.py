import random, math
from letterboxdpy.list import List as LBList
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.utils.utils_url import get_page_url
from letterboxdpy.utils.movies_extractor import extract_movies_from_vertical_list

def get_random_movie_from_list(user, slug):
    """
    Fetches a random movie from a Letterboxd list using an optimized paging strategy.
    Returns: (movie_dict, list_title, total_count)
    """
    # Initialize list to get metadata (count, title)
    # This only fetches the first page by default
    lb = LBList(user, slug)
    count = lb.get_count()
    
    if not count:
        return None, lb.title, 0
            
    # Optimization: Pick a random page (100 items per page) instead of fetching all
    total_pages = math.ceil(count / 100)
    random_page = random.randint(1, total_pages)
    
    page_url = get_page_url(lb.url, random_page)
    
    # Use internal scraper to get just this page's movies
    page_dom = parse_url(page_url)
    movies = extract_movies_from_vertical_list(page_dom)
    
    if not movies:
        return None, lb.title, count
            
    movie = random.choice(list(movies.values()))
    return movie, lb.title, count
