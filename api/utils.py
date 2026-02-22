import re, json

def extract_info(val):
    val = val.strip().lower()
    # Clean up standard URL prefixes
    val = re.sub(r'^https?://(www\.)?letterboxd\.com/', '', val)
    val = re.sub(r'^letterboxd\.com/', '', val)
    
    parts = [p for p in val.split('/') if p]
    
    # Format: user/list/slug
    if len(parts) >= 3 and parts[1] == 'list':
        return parts[0], parts[2]
    # Format: user/slug or user//slug
    elif len(parts) >= 2:
        # ignore generic pages like 'films' or 'followers' to avoid bugs if a user inputs something incomplete
        if parts[1] not in ('films', 'following', 'followers', 'reviews', 'lists', 'watchlist'):
            return parts[0], parts[1]
            
    return None, None

def get_error_msg(e):
    msg = str(e)
    try:
        # letterboxdpy throws JSON-structured errors, extract clean message
        return json.loads(msg.split('\n')[0]).get('message', msg)
    except:
        return msg
