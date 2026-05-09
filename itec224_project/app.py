from flask import Flask, render_template, request, jsonify
import threading
import scraper
import scheduler

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    members = [
        {
            "name": "Ayakoz Kanatnur",
            "student_number": "22300738",
            "hobbies": ["Reading", "playing musical instruments", "learning languages"],
            "image": "/static/images/ayo.jpg"
        },
        {
            "name": "Samuel P. Wleh Jr",
            "student_number": "22326885",
            "hobbies": ["Gaming", "Coding", "Music"],
            "image": "/static/images/sam.jpg"
        },
        {
            "name": "Nour Belahsen",
            "student_number": "22312227",
            "hobbies": ["Learning languages", "traveling"],
            "image": "/static/images/nour.jpg"
        },
        {
            "name": "Rashed Haylooz",
            "student_number": "22319110",
            "hobbies": ["Football", "Chess", "Cooking"],
            "image": "/static/images/rash.jpg"
        },
        {
            "name": "Abdullokh Akhmatkulov",
            "student_number": "22405343",
            "hobbies": ["Calisthenics", "boxing", "anime",  "gaming"],
            "image": "/static/images/na.jpg"
        },
        {
            "name": "Aitegin Shabaeva",
            "student_number": "22301356",
            "hobbies": ["volleyball", "reading", "watching movies"],
            "image": "/static/images/ai.jpeg"
        }
    ]
    return render_template('about.html', members=members)

@app.route('/task')
def task():
    return render_template('task.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url', '').strip()
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided.'})
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        result = scraper.scrape_and_send(url)
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Start the scheduler in a background thread
    t = threading.Thread(target=scheduler.start_scheduler, daemon=True)
    t.start()
    app.run(debug=True)
