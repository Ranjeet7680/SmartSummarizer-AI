"""
Simple Extractive Summarizer (No Model Download Required)
Uses frequency-based sentence scoring
"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class TextSummarizer:
    def __init__(self):
        """Initialize simple extractive summarizer"""
        print("🧠 Loading simple extractive summarizer...")
        self.stop_words = set(stopwords.words('english'))
        print("✅ Summarizer ready!")
    
    def summarize(self, text, length='medium'):
        """
        Summarize text using extractive method
        
        Args:
            text (str): Input text to summarize
            length (str): 'short', 'medium', or 'long'
        
        Returns:
            str: Summarized text
        """
        # Handle empty text
        if not text or len(text.strip()) == 0:
            return "No text to summarize."
        
        # Tokenize into sentences
        sentences = sent_tokenize(text)
        
        # If text is too short, return as is
        if len(sentences) <= 3:
            return text
        
        # Length mapping (number of sentences to include)
        length_map = {
            'short': max(2, len(sentences) // 5),
            'medium': max(3, len(sentences) // 3),
            'long': max(5, len(sentences) // 2)
        }
        
        num_sentences = length_map.get(length, length_map['medium'])
        
        # Calculate sentence scores
        sentence_scores = self._score_sentences(text, sentences)
        
        # Get top sentences
        top_sentences = sorted(
            sentence_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:num_sentences]
        
        # Sort by original order
        top_sentences = sorted(top_sentences, key=lambda x: sentences.index(x[0]))
        
        # Join sentences
        summary = ' '.join([s[0] for s in top_sentences])
        
        return summary
    
    def _score_sentences(self, text, sentences):
        """Score sentences based on word frequency"""
        # Tokenize and clean words
        words = word_tokenize(text.lower())
        words = [
            word for word in words
            if word not in self.stop_words
            and word not in string.punctuation
            and len(word) > 2
        ]
        
        # Calculate word frequencies
        word_freq = Counter(words)
        
        # Normalize frequencies
        max_freq = max(word_freq.values()) if word_freq else 1
        word_freq = {word: freq / max_freq for word, freq in word_freq.items()}
        
        # Score sentences
        sentence_scores = {}
        for sentence in sentences:
            sentence_words = word_tokenize(sentence.lower())
            sentence_words = [
                word for word in sentence_words
                if word in word_freq
            ]
            
            if sentence_words:
                # Average word score
                score = sum(word_freq[word] for word in sentence_words) / len(sentence_words)
                sentence_scores[sentence] = score
        
        return sentence_scores
    
    def _chunk_text(self, text, max_size):
        """Split text into chunks (not needed for simple summarizer but kept for compatibility)"""
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            if current_size + sentence_size > max_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_size = sentence_size
            else:
                current_chunk.append(sentence)
                current_size += sentence_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks


# Test function
if __name__ == "__main__":
    summarizer = TextSummarizer()
    
    test_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the 
    natural intelligence displayed by humans and animals. Leading AI textbooks define the field 
    as the study of "intelligent agents": any device that perceives its environment and takes 
    actions that maximize its chance of successfully achieving its goals. Colloquially, the term 
    "artificial intelligence" is often used to describe machines that mimic "cognitive" functions 
    that humans associate with the human mind, such as "learning" and "problem solving". As 
    machines become increasingly capable, tasks considered to require "intelligence" are often 
    removed from the definition of AI, a phenomenon known as the AI effect. A quip in Tesler's 
    Theorem says "AI is whatever hasn't been done yet." For instance, optical character 
    recognition is frequently excluded from things considered to be AI, having become a routine 
    technology.
    """
    
    print("\n📝 Original Text:")
    print(test_text)
    
    print("\n🎯 Summary:")
    summary = summarizer.summarize(test_text, 'short')
    print(summary)
