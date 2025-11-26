from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

def debug_layout(pdf_path):
    text = extract_text(pdf_path, laparams=LAParams())
    with open("layout_dump.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Layout dumped to layout_dump.txt")

if __name__ == "__main__":
    debug_layout("sntf.pdf")
