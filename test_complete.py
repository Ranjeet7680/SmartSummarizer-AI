"""
Complete test of PDF upload and summarization
"""

import requests
import os
import time

BASE_URL = "http://localhost:5000"

def test_pdf_upload_and_summarize():
    """Test complete workflow: PDF upload → Extract → Summarize"""
    
    print("🧪 COMPLETE TEST: PDF Upload → Extract → Summarize\n")
    print("=" * 60)
    
    # Check if test PDF exists
    pdf_file = "test_sample.pdf"
    if not os.path.exists(pdf_file):
        print(f"❌ {pdf_file} not found!")
        print("💡 Run: python create_test_pdf.py")
        return
    
    # Step 1: Upload PDF
    print("\n📤 Step 1: Uploading PDF...")
    try:
        with open(pdf_file, "rb") as f:
            files = {"file": (pdf_file, f, "application/pdf")}
            response = requests.post(f"{BASE_URL}/api/upload-pdf", files=files)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ PDF uploaded successfully!")
                print(f"📊 Extracted: {data['word_count']} words")
                print(f"📝 First 150 chars: {data['text'][:150]}...")
                
                extracted_text = data['text']
            else:
                print(f"❌ Upload failed: {data.get('error')}")
                return
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text)
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("\n" + "=" * 60)
    
    # Step 2: Summarize extracted text
    print("\n🤖 Step 2: Generating Summary...")
    
    for length in ['short', 'medium', 'long']:
        print(f"\n📏 Testing '{length}' summary...")
        try:
            response = requests.post(
                f"{BASE_URL}/api/summarize",
                json={"text": extracted_text, "length": length}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ {length.capitalize()} summary generated!")
                    print(f"   Original: {data['original_length']} words")
                    print(f"   Summary: {data['summary_length']} words")
                    reduction = (1 - data['summary_length']/data['original_length']) * 100
                    print(f"   Reduction: {reduction:.1f}%")
                    print(f"   Text: {data['summary'][:100]}...")
                else:
                    print(f"❌ Failed: {data.get('error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(0.5)  # Small delay between requests
    
    print("\n" + "=" * 60)
    print("\n✅ COMPLETE TEST FINISHED!")
    print("\n💡 Now test in browser: http://localhost:5000")
    print("   1. Drag & drop test_sample.pdf")
    print("   2. Click 'Summarize'")
    print("   3. Try different lengths (Short/Medium/Long)")

if __name__ == "__main__":
    test_pdf_upload_and_summarize()
