#!/usr/bin/env python
# /python/ocr.py

import sys
import re
from docx import Document

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text.strip())
    return "\n".join(full_text)

# Use the file path passed from Node, or default if not provided
if len(sys.argv) > 1:
    docx_path = sys.argv[1]
else:
    docx_path = r"/Users/gayatrikrishnakumar/Documents/Interdepartmental EL/python/Structured_TOC.docx"

extracted_text = extract_text_from_docx(docx_path)
print("=== Extracted Text ===")
print(extracted_text)

# Regex to extract Marks and BT Level
pattern = re.compile(r"Marks:\s*(\d+)\s*\nBT Level:\s*L(\d)")
matches = pattern.findall(extracted_text)

print("\n=== Extracted BT Levels ===")
if not matches:
    print("⚠️ No BT levels found. Check text formatting or tweak regex.")
else:
    for idx, (marks, bt_level) in enumerate(matches, start=1):
        print(f"Question {idx}: Marks = {marks}, BT Level = L{bt_level}")
