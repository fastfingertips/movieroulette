import random, math
from letterboxdpy.list import List as LBList
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.utils.utils_url import get_page_url
from letterboxdpy.utils.movies_extractor import extract_movies_from_vertical_list

def get_list_metadata(user, slug):
    """Returns (lb_instance, title, count)"""
    lb = LBList(user, slug)
    return lb, lb.title, lb.get_count()


def custom_extract_movies(dom):
    """
    A more robust extractor that gets posters and ratings 
    which the default letterboxdpy might miss.
    """
    items = dom.find_all("li", {"class": "posteritem"}) or dom.find_all("li", {"class": "griditem"})
    movies = {}
    
    for item in items:
        # Get the container with data attributes
        container = item.find("div", {"class": "react-component"}) or item
        if not container or 'data-film-id' not in container.attrs:
            continue
            
        movie_id = container['data-film-id']
        slug = container.get('data-item-slug') or container.get('data-film-slug')
        name = container.get('data-item-name') or (container.img['alt'] if container.img else "Unknown")
        
        # Poster Image
        img = container.find("img")
        poster = img.get('src') if img else None
        
        # Rating (Stars) - usually in the anchor's title or data-original-title
        link = container.find("a", {"class": "frame"})
        rating_text = link.get('data-original-title', '') if link else ''
        stars = ""
        if "★" in rating_text or "½" in rating_text:
            # Extract just the star part (e.g. "Title ★★★" -> "★★★")
            parts = rating_text.split(" ")
            stars = parts[-1] if parts else ""

        movies[movie_id] = {
            "slug": slug,
            "name": name,
            "poster": poster,
            "stars": stars,
            'url': f'https://letterboxd.com/film/{slug}/'
        }
    return movies

def get_random_from_instance(lb, count):
    """Picks a random movie from an existing LBList instance using paging logic"""
    if not count:
        return None
            
    total_pages = math.ceil(count / 100)
    random_page = random.randint(1, total_pages)
    
    page_dom = parse_url(get_page_url(lb.url, random_page))
    
    # Use our custom extractor for more data (poster, stars)
    movies = custom_extract_movies(page_dom)
    
    return random.choice(list(movies.values())) if movies else None


