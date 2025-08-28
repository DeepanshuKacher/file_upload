from flask import Flask, request, jsonify, render_template, send_from_directory
import os

app = Flask(__name__)

# Upload and Share folders
UPLOAD_FOLDER = 'uploads'
SHARE_FOLDER = 'share'

for folder in [UPLOAD_FOLDER, SHARE_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SHARE_FOLDER'] = SHARE_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('files')
    if not files or all(f.filename == '' for f in files):
        return jsonify({'error': 'No selected files'}), 400

    saved_files = []
    for file in files:
        if file and file.filename:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            saved_files.append(file.filename)

    return jsonify({'message': 'Files uploaded successfully', 'files': saved_files}), 200


# Route to list shareable files
@app.route('/share', methods=['GET'])
def list_shared_files():
    files = os.listdir(app.config['SHARE_FOLDER'])
    return jsonify({'files': files})


# Route to download a file
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['SHARE_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
