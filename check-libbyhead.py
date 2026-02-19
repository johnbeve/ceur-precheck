#
# File: check-libbyhead.py
# Version: 0.98
#
# Checks whether the PDF files in the current directory have issues in matching the CEURART style.
# (C) 2024-2026 by Manfred Jeusfeld. This script is made available under the
# Creative Commons Attribution-ShareAlike CC-BY-SA 4.0 license.
#
# Call by python3 $HOME/bin/check-libbyhead.py <pdffile> 
# Returns exit code 0 if the headings on page 1 of the pdffile are in Libertinus Sans font
# and the body text is in Libertinus Serif font.
# Returns exit code 1 if headings are not in Libertinus Sans.
# Returns exit code 2 if body text is not in Libertinus Serif.
# Returns exit code 3 if body text is not in Libertinus Serif and headings are not in Libertinus Sans.
#
# Created with the help of GenAI; requires python3 and pdfminer.six
#  pip install pdfminer.six
#
# 2026-01-08: Have a dedicated BODY_SIZE_FACTOR to identify the body text.
#

import sys
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTAnno, LTTextBox, LTTextLine
import statistics
import logging
import re

# Configure pdfminer.six to suppress its own logging output
logging.getLogger('pdfminer').setLevel(logging.WARNING)

# --- Hardcoded Parameters ---
TARGET_HEADING_FONT_PATTERNS = [
    r'LibertinusSans', r'LibertinusSans-Regular', r'LibertinusSans-Bold',
    r'[A-Z0-9]{6,}\\+LibertinusSans', r'[A-Z0-9]{6,}\\+LibertinusSans-Bold', r'CIDFont\\.F[0-9]+', r'/LibertinusSans'
]
TARGET_BODY_FONT_PATTERNS = [
    r'LibertinusSerif', r'LibertinusSerif-Regular', r'LibertinusSerif-Italic',
    r'[A-Z0-9]{6,}\\+LibertinusSerif', r'[A-Z0-9]{6,}\\+LibertinusSerif-Regular', r'CIDFont\\.F[0-9]+', r'/LibertinusSerif'
]
HEADING_SIZE_FACTOR = 1.35       # Check fonts 35% larger than the body text
BODY_SIZE_FACTOR = 1.05        # Check fonts smaller than 105% of the body text
SUCCESS_THRESHOLD = 0.80 # 80% usage of the target font in headings and body required
PAGES_TO_CHECK = [0]     # Only check the first page (index 0)
# ----------------------------

def get_all_chars(layout):
    """
    Helper function to recursively yield all LTChar objects from a layout element.
    """
    for item in layout:
        if isinstance(item, LTChar):
            yield item
        elif isinstance(item, (LTTextBox, LTTextLine)):
            yield from get_all_chars(item)
        elif hasattr(item, '__iter__'):
            yield from get_all_chars(item)

def check_font_usage_headings_p1(pdf_path: str):
    # 1. First Pass: Collect all font sizes for heuristic determination (Page 1 only)
    all_font_sizes = []
    all_font_names = set()

    for page_layout in extract_pages(pdf_path, page_numbers=PAGES_TO_CHECK):
        for character in get_all_chars(page_layout):
            all_font_sizes.append(character.size)
            all_font_names.add(character.fontname)

    try:
        body_font_size = statistics.mode(all_font_sizes)
    except statistics.StatisticsError:
        body_font_size = statistics.median(all_font_sizes)

    heading_size_threshold = body_font_size * HEADING_SIZE_FACTOR

    # 2. Second Pass: Check only characters above the heading size threshold (Page 1 only)
    heading_chars_total = 0
    heading_chars_target = 0
    heading_font_names = set()

    for page_layout in extract_pages(pdf_path, page_numbers=PAGES_TO_CHECK):
        for character in get_all_chars(page_layout):
            if character.size >= heading_size_threshold:
                heading_chars_total += 1
                font_name = character.fontname
                heading_font_names.add(font_name)
                if any(re.search(pattern, font_name, re.IGNORECASE) for pattern in TARGET_HEADING_FONT_PATTERNS):
                    heading_chars_target += 1

    if heading_chars_total == 0:
        return False, 0.0, 0, all_font_names, heading_font_names

    # 3. Calculate and return success/failure
    usage_percentage = heading_chars_target / heading_chars_total

    return (
        usage_percentage >= SUCCESS_THRESHOLD,
        usage_percentage,
        heading_chars_total,
        all_font_names,
        heading_font_names
    )

def check_font_usage_body_p1(pdf_path: str):
    # 1. First Pass: Collect all font sizes for heuristic determination (Page 1 only)
    all_font_sizes = []
    all_font_names = set()

    for page_layout in extract_pages(pdf_path, page_numbers=PAGES_TO_CHECK):
        for character in get_all_chars(page_layout):
            all_font_sizes.append(character.size)
            all_font_names.add(character.fontname)

    try:
        body_font_size = statistics.mode(all_font_sizes)
    except statistics.StatisticsError:
        body_font_size = statistics.median(all_font_sizes)

    body_size_threshold = body_font_size * BODY_SIZE_FACTOR

    # 2. Second Pass: Check only characters below the heading size threshold (Page 1 only)
    body_chars_total = 0
    body_chars_target = 0
    body_font_names = set()

    for page_layout in extract_pages(pdf_path, page_numbers=PAGES_TO_CHECK):
        for character in get_all_chars(page_layout):
            if character.size <= body_size_threshold:
                body_chars_total += 1
                font_name = character.fontname
                body_font_names.add(font_name)
                if any(re.search(pattern, font_name, re.IGNORECASE) for pattern in TARGET_BODY_FONT_PATTERNS):
                    body_chars_target += 1

    if body_chars_total == 0:
        return False, 0.0, 0, all_font_names, body_font_names

    # 3. Calculate and return success/failure
    usage_percentage = body_chars_target / body_chars_total

    return (
        usage_percentage >= SUCCESS_THRESHOLD,
        usage_percentage,
        body_chars_total,
        all_font_names,
        body_font_names
    )

# --- Execution Block (Minimal Output) ---
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <path_to_pdf>", file=sys.stderr)
        sys.exit(1)

    pdf_file = sys.argv[1]

    headings_passed, headings_usage, headings_total, all_fonts, heading_fonts = check_font_usage_headings_p1(pdf_file)
    body_passed, body_usage, body_total, _, body_fonts = check_font_usage_body_p1(pdf_file)

    # Debug output (uncomment as needed)
#    print(f"DEBUG: {pdf_file}")
#    print(f"DEBUG: All fonts: {all_fonts}")
#    print(f"DEBUG: Heading fonts: {heading_fonts}")
#    print(f"DEBUG: Body fonts: {body_fonts}")
#    print(f"DEBUG: Headings usage: {headings_usage:.2f}, Total: {headings_total}")
#    print(f"DEBUG: Body usage: {body_usage:.2f}, Total: {body_total}")

    if headings_passed and body_passed:
#        print(f"PASS: Headings use LibertinusSans and body text uses LibertinusSerif.")
        sys.exit(0)
    elif not headings_passed and body_passed:
#        print(f"FAIL: Headings do NOT use LibertinusSans.")
        sys.exit(1)
    elif headings_passed and not body_passed:
#        print(f"Body text does NOT use LibertinusSerif.")
        sys.exit(2)
    else:
#        print(f"FAIL: Headings and body text do NOT use LibertinusSans/Serif.")
        sys.exit(3)
