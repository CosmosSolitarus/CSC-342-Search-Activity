from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__, template_folder='../www/templates', static_folder='../www/static')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return render_template('home.html')

# handles search requests
@app.route('/search', methods=['POST'])
def search_tracks():
    data = load_json_data()

    # this comes from search.js
    filters = request.json
    search_by = filters.get('searchBy')
    sort_by = filters.get('sortBy')
    include_explicit = filters.get('includeExplicit')
    search_text = filters.get('searchText').lower() # convert all searches and titles (later) to lower case

    # filter by title/artists/genres and search text
    if search_by == 'title':
        filtered_data = [track for track in data if search_text in track['title'].lower()]
    elif search_by == 'artists':
        filtered_data = [track for track in data if any(search_text in artist.lower() for artist in track['artists'])]
    elif search_by == 'genres':
        filtered_data = [track for track in data if search_text in track['genres'].lower()]
    else:
        filtered_data = data

    # explicit content filter
    if not include_explicit:
        filtered_data = [track for track in filtered_data if track.get('explicit', False)]

    # sort
    if sort_by == 'popularity':
        filtered_data.sort(key=lambda x: x['popularity'], reverse=True)
    elif sort_by == 'duration_mins':
        filtered_data.sort(key=lambda x: x['duration_mins'])

    return jsonify(filtered_data)

# load and combine json files
def load_json_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # gets the dir of app.py to find json files
    file1_path = os.path.join(base_dir, '../www/static/data/top_tracks_2023.json')
    file2_path = os.path.join(base_dir, '../www/static/data/top_tracks_2024.json')

    with open(file1_path) as file1, \
         open(file2_path) as file2:
        data_2023 = json.load(file1)
        data_2024 = json.load(file2)
    
    return data_2023 + data_2024