"""
Test script to verify PDF upload and summarization
"""

import requests
import os

# Test with a sample PDF (you'll need to provide one)
# Or test with text directly

def test_text_summarization():
    """Test text summarization endpoint"""
    url = "http://localhost:5000/api/summarize"
    
    test_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the 
    natural intelligence displayed by humans and animals. Leading AI textbooks define the field 
    as the study of intelligent agents: any device that perceives its environment and takes 
    actions that maximize its chance of successfully achieving its goals. Colloquially, the term 
    artificial intelligence is often used to describe machines that mimic cognitive functions 
    that humans associate with the human mind, such as learning and problem solving. As 
    machines become increasingly capable, tasks considered to require intelligence are often 
    removed from the definition of AI, a phenomenon known as the AI effect. A quip in Tesler's 
    Theorem says AI is whatever hasn't been done yet. For instance, optical character 
    recognition is frequently excluded from things considered to be AI, having become a routine 
    technology. Modern machine learning techniques are effective at performing a wide range of 
    tasks. Deep learning has dramatically improved the performance of programs in many important 
    subfields of artificial intelligence, including computer vision, speech recognition, image 
    classification and others.
    """
    
    data = {
        "text": test_text,
        "length": "medium"
    }
    
    print("🧪 Testing text summarization...")
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"\n📝 Original ({result['original_length']} words):")
            print(test_text[:200] + "...")
            print(f"\n🎯 Summary ({result['summary_length']} words):")
            print(result['summary'])
            print(f"\n📊 Reduction: {100 - (result['summary_length']/result['original_length']*100):.1f}%")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"❌ Error: {e}")

def test_pdf_upload():
    """Test PDF upload endpoint"""
    url = "http://localhost:5000/api/upload-pdf"
    
    # Check if test PDF exists
    if not os.path.exists("test.pdf"):
        print("⚠️ No test.pdf found. Please create one or provide a PDF file.")
        print("💡 You can test PDF upload manually through the web interface.")
        return
    
    print("🧪 Testing PDF upload...")
    try:
        with open("test.pdf", "rb") as f:
            files = {"file": ("test.pdf", f, "application/pdf")}
            response = requests.post(url, files=files)
            
        if response.status_code == 200:
            result = response.json()
            print("✅ PDF uploaded successfully!")
            print(f"📄 Extracted {result['word_count']} words")
            print(f"\n📝 First 200 characters:")
            print(result['text'][:200] + "...")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 SmartSummarizer API Test\n")
    print("=" * 50)
    
    # Test text summarization
    test_text_summarization()
    
    print("\n" + "=" * 50 + "\n")
    
    # Test PDF upload
    test_pdf_upload()
    
    print("\n" + "=" * 50)
    print("\n✅ Testing complete!")
    print("💡 Open http://localhost:5000 to test in browser")
