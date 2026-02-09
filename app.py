from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os, json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = "supersecretkey"  

ADMIN_PASSWORD = "hmahma"


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data', exist_ok=True)
if not os.path.exists('data/announcements.json'):
    with open('data/announcements.json', 'w') as f:
        json.dump([], f)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Admin login
@app.route('/admin_login', methods=['POST'])
def admin_login():
    password = request.form.get('password')
    if password == ADMIN_PASSWORD:
        return jsonify({"success": True})
    return jsonify({"success": False})

# Add announcement
@app.route('/add_announcement', methods=['POST'])
def add_announcement():
    data = request.get_json()
    text = data.get('text')
    date = data.get('date')
    if text and date:
        with open('data/announcements.json', 'r') as f:
            announcements = json.load(f)
        announcements.append({"text": text, "date": date})
        with open('data/announcements.json', 'w') as f:
            json.dump(announcements, f)
        return jsonify({"success": True})
    return jsonify({"success": False})

# Delete announcement
@app.route('/delete_announcement', methods=['POST'])
def delete_announcement():
    data = request.get_json()
    index = data.get('index')
    with open('data/announcements.json', 'r') as f:
        announcements = json.load(f)
    if 0 <= index < len(announcements):
        announcements.pop(index)
        with open('data/announcements.json', 'w') as f:
            json.dump(announcements, f)
        return jsonify({"success": True})
    return jsonify({"success": False})

# Get announcements
@app.route('/get_announcements')
def get_announcements():
    with open('data/announcements.json', 'r') as f:
        announcements = json.load(f)
    return jsonify(announcements)

# Upload notes
@app.route('/upload_note', methods=['POST'])
def upload_note():
    if 'note' in request.files:
        file = request.files['note']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({"success": True, "filename": file.filename})
    return jsonify({"success": False})

# List notes
@app.route('/get_notes')
def get_notes():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

# Download note
@app.route('/download_note/<filename>')
def download_note(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

