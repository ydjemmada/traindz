import sys
from pypdf import PdfReader

def analyze_all_pages(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        print(f"Number of pages: {len(reader.pages)}")
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            print(f"\n--- Page {i+1} ---\n")
            # Print first 200 chars to identify the line
            print(text[:200]) 
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_all_pages("sntf.pdf")
