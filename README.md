# 🚀 SmartSummarizer AI

**Advanced Text Summarization App** powered by RNN/Transformer models with interactive UI

## ✨ Features

- 📄 **PDF Upload** - Drag & drop or browse PDF files
- ✍️ **Text Input** - Direct text input support
- 🧠 **AI-Powered** - Uses BART (Transformer) model for high-quality summaries
- 🎛️ **Length Control** - Choose between Short, Medium, or Long summaries
- 🎨 **Modern UI** - Smooth animations and dark/light mode
- 📊 **Statistics** - Word count, character count, and reduction percentage
- 📋 **Copy to Clipboard** - One-click copy functionality

## 🛠️ Tech Stack

### Backend
- **Flask** - Web framework
- **Transformers** (HuggingFace) - BART model for summarization
- **PyMuPDF** - PDF text extraction
- **NLTK** - Text processing

### Frontend
- **HTML5/CSS3** - Modern responsive design
- **Vanilla JavaScript** - No framework dependencies
- **CSS Animations** - Smooth transitions and effects

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup Steps

1. **Clone or download this project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open in browser**
```
http://localhost:5000
```

## 🎯 Usage

1. **Upload PDF** or **Paste Text**
   - Drag & drop a PDF file
   - Or paste your text directly

2. **Select Summary Length**
   - Short (30-100 words)
   - Medium (50-200 words)
   - Long (100-400 words)

3. **Click "Summarize"**
   - AI will generate your summary
   - View statistics and reduction percentage

4. **Copy Summary**
   - Click the copy button to copy to clipboard

## 🧠 Model Information

This app uses **facebook/bart-large-cnn** model:
- Pre-trained on CNN/DailyMail dataset
- State-of-the-art summarization quality
- Handles long documents efficiently

## 📁 Project Structure

```
SmartSummarizer/
├── app.py                 # Flask backend
├── summarizer.py          # Summarization logic
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML page
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend logic
└── uploads/              # Temporary PDF storage
```

## 🎨 Features Breakdown

### PDF Processing
- Extracts text from multi-page PDFs
- Handles various PDF formats
- Automatic cleanup after processing

### Smart Summarization
- Chunks long texts automatically
- Adjusts summary length dynamically
- Handles edge cases (very short/long texts)

### Interactive UI
- Real-time word/character count
- Drag & drop file upload
- Loading animations
- Toast notifications
- Dark/Light theme toggle

## 🔧 Configuration

### Adjust Summary Parameters
Edit `summarizer.py`:
```python
length_params = {
    'short': {'max_length': 100, 'min_length': 30},
    'medium': {'max_length': 200, 'min_length': 50},
    'long': {'max_length': 400, 'min_length': 100}
}
```

### Change Model
Replace in `summarizer.py`:
```python
self.model = pipeline("summarization", model="facebook/bart-large-cnn")
# Try: "t5-base", "google/pegasus-xsum", etc.
```

## 🚀 Advanced Features (Future)

- [ ] Voice output (Text-to-Speech)
- [ ] Multiple language support
- [ ] Bullet point summaries
- [ ] Keyword extraction
- [ ] Summary confidence score
- [ ] Export to PDF/DOCX
- [ ] API endpoints for integration

## 📱 Mobile Support

Fully responsive design works on:
- Desktop browsers
- Tablets
- Mobile phones

## 🐛 Troubleshooting

### Model Download Issues
First run downloads ~1.6GB model. Ensure stable internet.

### PDF Extraction Errors
Some PDFs (scanned images) may not extract text. Use OCR-enabled PDFs.

### Memory Issues
For very large texts, the app automatically chunks them.

## 📄 License

MIT License - Free to use and modify

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 💡 Tips

1. **Best Results**: Use well-formatted text (proper paragraphs)
2. **PDF Quality**: Text-based PDFs work best
3. **Length**: 100-5000 words gives optimal summaries
4. **Speed**: First run is slower (model loading)

## 🎓 Learning Resources

- [Transformers Documentation](https://huggingface.co/docs/transformers)
- [BART Paper](https://arxiv.org/abs/1910.13461)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Built with ❤️ using Flask + Transformers + Modern Web Tech**

🌟 Star this project if you find it useful!
