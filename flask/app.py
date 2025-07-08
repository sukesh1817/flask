from flask import Flask, request, jsonify, session
from werkzeug.utils import secure_filename
import os
from utils.document_processor import analyze_prompt_with_document
import uuid
from flask import render_template

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit
app.secret_key = 'xg7x6trx23gr273rwefw'  # Set a strong secret key!
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        random_hash = uuid.uuid4().hex
        filename = f"{random_hash}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        session['document_name'] = filename  # Store in session
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

    return jsonify({'message': 'Invalid file format'}), 400


@app.route('/api/analyse', methods=['POST'])
def analyse():
    data = request.get_json()
    prompt = data.get('prompt_input')
    # Retrieve document name from session
    document_name = session.get('document_name')

    if not prompt or not document_name:
        return jsonify({'message': 'Prompt and document name are required'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(document_name))
    if not os.path.exists(filepath):
        return jsonify({'message': 'Document not found'}), 404

    try:
        response = analyze_prompt_with_document(prompt, filepath)
        return jsonify({'result': response}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
