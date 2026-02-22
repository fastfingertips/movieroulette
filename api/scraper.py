import random, math
from letterboxdpy.list import List as LBList
from letterboxdpy.movie import Movie as LBMovie
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.utils.utils_url import get_page_url
from letterboxdpy.utils.movies_extractor import extract_movies_from_vertical_list

def get_list_metadata(user, slug):
    """Returns (lb_instance, title, count) using total library structure"""
    lb = LBList(user, slug)
    return lb, lb.title, lb.get_count()

def get_random_from_instance(lb, count):
    """
    Picks a random movie from an existing LBList instance.
    Uses library's Movie object for rich data.
    """
    if not count:
        return None
            
    # 1. Get random page content
    total_pages = math.ceil(count / 100)
    random_page = random.randint(1, total_pages)
    page_dom = parse_url(get_page_url(lb.url, random_page))
    
    # 2. Use library's built-in extractor to get the slugs
    movies_meta = extract_movies_from_vertical_list(page_dom)
    if not movies_meta:
        return None
            
    # 3. Pick a random candidate from the page
    candidate_id = random.choice(list(movies_meta.keys()))
    candidate_meta = movies_meta[candidate_id] # Contains {slug, name, year, url}
    
    # 4. Use library's Movie structure for full rich data (Poster, Rating, etc.)
    # This ensures we get the "ready-made" object data as requested
    movie = LBMovie(candidate_meta['slug'])
    
    return {
        "name": movie.title,
        "year": movie.year,
        "slug": movie.slug,
        "url": movie.url,
        "poster": movie.poster,
        "rating": movie.rating
    }
