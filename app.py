from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

SPACEX_API_URL = "https://api.spacexdata.com/v4/launches/"
ITEMS_PER_PAGE = 5

@app.route('/')
@app.route('/page/<int:page>')
def index(page=1):
    response = requests.get(SPACEX_API_URL)
    if response.status_code == 200:
        launches = response.json()
        total_launches = len(launches)
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        paginated_launches = launches[start:end]
        total_pages = (total_launches + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        return render_template('index.html', launches=paginated_launches, page=page, total_pages=total_pages)
    else:
        return "Could not fetch launches", 500

@app.route('/launch/<launch_id>')
def launch(launch_id):
    response = requests.get(f"{SPACEX_API_URL}{launch_id}")
    if response.status_code == 200:
        launch_data = response.json()
        youtube_link = None
        if 'links' in launch_data and 'youtube_id' in launch_data['links']:
            youtube_id = launch_data['links']['youtube_id']
            youtube_link = f"https://www.youtube.com/embed/{youtube_id}"
        return render_template('launch.html', launch=launch_data, youtube_link=youtube_link)
    else:
        return "Launch not found", 404

if __name__ == '__main__':
    app.run(debug=True)
