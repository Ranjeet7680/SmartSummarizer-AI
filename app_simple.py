"""
Simple version - No model download required!
Uses extractive summarization (instant start)
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import fitz  # PyMuPDF
import os
from summarizer_simple import TextSummarizer

app = Flask(__name__)
CORS(app)

# Initialize summarizer (instant - no download)
summarizer = TextSummarizer()

# Upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/summarize', methods=['POST'])
def summarize_text():
    try:
        data = request.json
        text = data.get('text', '')
        length = data.get('length', 'medium')  # short, medium, long
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Generate summary
        summary = summarizer.summarize(text, length)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'original_length': len(text.split()),
            'summary_length': len(summary.split())
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'success': False, 'error': 'Only PDF files allowed'}), 400
        
        # Check file size (max 10MB)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            return jsonify({'success': False, 'error': 'File too large (max 10MB)'}), 400
        
        # Save file with unique name
        import time
        filename = f"upload_{int(time.time())}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from PDF
        text = extract_text_from_pdf(filepath)
        
        # Clean up
        try:
            os.remove(filepath)
        except:
            pass
        
        if not text or len(text.strip()) == 0:
            return jsonify({'success': False, 'error': 'No text found in PDF. It might be an image-based PDF.'}), 400
        
        return jsonify({
            'success': True,
            'text': text,
            'word_count': len(text.split())
        })
    
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return jsonify({'success': False, 'error': f'Error processing PDF: {str(e)}'}), 500

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text()
            text += page_text + "\n\n"
        
        doc.close()
        
        # Clean up text
        text = text.strip()
        # Remove excessive whitespace
        import re
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

if __name__ == '__main__':
    print("🚀 SmartSummarizer AI (Simple Version) is starting...")
    print("⚡ No model download required - Instant start!")
    print("📍 Open: http://localhost:5000")
    print("\n💡 Tip: For AI-powered summaries, use 'python app.py' instead")
    app.run(debug=True, host='0.0.0.0', port=5000)
