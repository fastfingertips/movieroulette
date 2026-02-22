import random, math
from letterboxdpy.list import List as LBList
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.utils.utils_url import get_page_url
from letterboxdpy.utils.movies_extractor import extract_movies_from_vertical_list

def get_list_metadata(user, slug):
    """Returns (lb_instance, title, count)"""
    lb = LBList(user, slug)
    return lb, lb.title, lb.get_count()

def get_random_from_instance(lb, count):
    """Picks a random movie from an existing LBList instance using paging logic"""
    if not count:
        return None
            
    total_pages = math.ceil(count / 100)
    random_page = random.randint(1, total_pages)
    
    page_dom = parse_url(get_page_url(lb.url, random_page))
    movies = extract_movies_from_vertical_list(page_dom)
    
    return random.choice(list(movies.values())) if movies else None

