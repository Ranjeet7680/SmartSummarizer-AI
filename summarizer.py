import nltk
from transformers import pipeline
import warnings

warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

class TextSummarizer:
    def __init__(self):
        """Initialize the summarizer with transformer model"""
        print("🧠 Loading summarization model...")
        # Using smaller, faster model for better performance
        # Options: "sshleifer/distilbart-cnn-12-6" (faster) or "facebook/bart-large-cnn" (better quality)
        self.model = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        print("✅ Model loaded successfully!")
    
    def summarize(self, text, length='medium'):
        """
        Summarize text with specified length
        
        Args:
            text (str): Input text to summarize
            length (str): 'short', 'medium', or 'long'
        
        Returns:
            str: Summarized text
        """
        # Handle empty text
        if not text or len(text.strip()) == 0:
            return "No text to summarize."
        
        # Split into sentences for better processing
        sentences = nltk.sent_tokenize(text)
        word_count = len(text.split())
        
        # If text is too short, return as is
        if word_count < 50:
            return text
        
        # Set length parameters based on selection
        length_params = {
            'short': {
                'max_length': min(100, word_count // 4),
                'min_length': min(30, word_count // 8)
            },
            'medium': {
                'max_length': min(200, word_count // 3),
                'min_length': min(50, word_count // 6)
            },
            'long': {
                'max_length': min(400, word_count // 2),
                'min_length': min(100, word_count // 4)
            }
        }
        
        params = length_params.get(length, length_params['medium'])
        
        # Handle very long texts by chunking
        max_chunk_size = 1024  # Model's max input size
        
        if len(text) > max_chunk_size:
            # Split into chunks
            chunks = self._chunk_text(text, max_chunk_size)
            summaries = []
            
            for chunk in chunks:
                try:
                    result = self.model(
                        chunk,
                        max_length=params['max_length'] // len(chunks),
                        min_length=params['min_length'] // len(chunks),
                        do_sample=False
                    )
                    summaries.append(result[0]['summary_text'])
                except Exception as e:
                    print(f"Error summarizing chunk: {e}")
                    continue
            
            return ' '.join(summaries)
        else:
            # Summarize directly
            try:
                result = self.model(
                    text,
                    max_length=params['max_length'],
                    min_length=params['min_length'],
                    do_sample=False
                )
                return result[0]['summary_text']
            except Exception as e:
                return f"Error generating summary: {str(e)}"
    
    def _chunk_text(self, text, max_size):
        """Split text into chunks of maximum size"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            if current_size + word_size > max_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
