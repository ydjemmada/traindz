import sys
from pypdf import PdfReader

def analyze_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        print(f"Number of pages: {len(reader.pages)}")
        
        # Extract text from the first 2 pages
        for i in range(min(2, len(reader.pages))):
            page = reader.pages[i]
            text = page.extract_text()
            print(f"\n--- Page {i+1} ---\n")
            print(text[:1000]) # Print first 1000 chars
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_pdf("sntf.pdf")
