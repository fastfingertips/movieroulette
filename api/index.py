from flask import Flask, request, jsonify
import random, os

# Try relative imports for Vercel / package context, 
# fall back to direct imports for local script execution
try:
    from .utils import extract_info, get_error_msg
    from .scraper import get_random_movie_from_list
except ImportError:
    from utils import extract_info, get_error_msg
    from scraper import get_random_movie_from_list

# Absolute path to the folder containing index.html (the project root)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Initialize Flask with the project root as the static folder
app = Flask(__name__, static_folder=ROOT_DIR, static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api', methods=['POST'])
def randomize():
    try:
        urls = [u.strip() for u in (request.json or {}).get('urls', []) if u.strip()]
        if not urls: 
            return jsonify({"error": "No URLs provided"}), 400
            
        url = random.choice(urls)
        user, slug = extract_info(url)
        if not user: 
            return jsonify({"error": f"Invalid URL: {url}"}), 400
            
        # Get random movie using the optimized scraper logic
        movie, title, count = get_random_movie_from_list(user, slug)
        
        if not movie:
            return jsonify({"error": "List is empty or inaccessible"}), 404
            
        return jsonify({
            "movie": {k: movie.get(k) for k in ['name', 'url', 'year']},
            "list": {"title": title, "count": count, "url": url}
        })
    except Exception as e:
        return jsonify({"error": get_error_msg(e)}), 500

if __name__ == "__main__":
    print(f"🚀 Starting server from: {ROOT_DIR}")
    # Using port 5050 to avoid any potential port 5000 conflicts
    app.run(port=5050, debug=True)
