import os
import re
from bs4 import BeautifulSoup
import codecs
import glob

# Mapping of file prefixes to English book names
BOOK_NAMES = {
    "x01": "Genesis",
    "x02": "Exodus",
    "x03": "Leviticus",
    "x04": "Numbers",
    "x05": "Deuteronomy",
    "x06": "Joshua",
    "x07": "Judges",
    "x08a": "Samuel I",
    "x08b": "Samuel II",
    "x09a": "Kings I",
    "x09b": "Kings II",
    "x10": "Isaiah",
    "x11": "Jeremiah",
    "x12": "Ezekiel",
    "x13": "Hosea",
    "x14": "Joel",
    "x15": "Amos",
    "x16": "Obadiah",
    "x17": "Jonah",
    "x18": "Micah",
    "x19": "Nahum",
    "x20": "Habakkuk",
    "x21": "Zephaniah",
    "x22": "Haggai",
    "x23": "Zechariah",
    "x24": "Malachi",
    "x25a": "Chronicles I",
    "x25b": "Chronicles II",
    "x26": "Psalms",
    "x26a": "Psalms 10",
    "x26b": "Psalms 11",
    "x26c": "Psalms 12",
    "x26d": "Psalms 13",
    "x26e": "Psalms 14",
    "x26f": "Psalms 15",
    "x27": "Job",
    "x28": "Proverbs",
    "x29": "Ruth",
    "x30": "Song of Songs", 
    "x31": "Ecclesiastes",
    "x32": "Lamentations",
    "x33": "Esther",
    "x34": "Daniel",
    "x35a": "Ezra",
    "x35b": "Nehemiah"
}


def extract_text_from_html(file_path):
    """Extract the text content from an HTML file, removing verse numbers and special markers."""
    with codecs.open(file_path, 'r', 'windows-1255') as file:
        try:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')

            # Find all P tags which contain the verses
            paragraphs = soup.find_all('p')

            text = []
            for p in paragraphs:
                # Skip elements with class 'tiny', 'm', or 's' as they are metadata
                if p.get('class') and any(cls in ['tiny', 'm', 's'] for cls in p.get('class')):
                    continue

                # First, remove all B tags (verse numbers)
                for b_tag in p.find_all('b'):
                    b_tag.decompose()

                # Extract text
                p_text = p.get_text(separator=' ')

                # Remove any content inside curly braces {}, including the braces
                p_text = re.sub(r'\{[^}]*\}', '', p_text)

                # Clean up extra spaces and line breaks
                p_text = re.sub(r'\s+', ' ', p_text).strip()

                if p_text:
                    text.append(p_text)

            return "\n\n".join(text)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return ""


def process_full_text(text):
    """Process text for the full version, removing words in parentheses."""
    # Pattern to find a word followed by parenthetical alternative
    # Then replace both with just the original word
    return re.sub(r'(\S+)\s*\([^)]*\)', r'\1', text)


def process_hesher_text(text):
    """Process text for the hesher version, replacing words with their parenthetical alternatives."""
    # Pattern to find a word followed by parenthetical alternative
    # Then replace both with just the parenthetical content (without parentheses)
    return re.sub(r'(\S+)\s*\(([^)]*)\)', r'\2', text)


def clean_text(text):
    """Remove non-alphabetic characters and handle dashes properly."""
    # Replace both single and double dashes with a space
    text = re.sub(r'--', ' ', text)
    text = re.sub(r'-', ' ', text)

    # Hebrew chars range: \u0590-\u05FF, also keep spaces and newlines
    text = re.sub(r'[^\u0590-\u05FF\s]', '', text)

    # Clean up extra spaces that might have been created
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def get_book_and_chapter(filename):
    """Extract book name and chapter number from filename."""
    # For files like x0101.htm (non-split books)
    match1 = re.match(r'x(\d{2})(\d{2})\.htm', filename)
    if match1:
        book_prefix = f"x{match1.group(1)}"
        chapter_num = match1.group(2)
        book_name = BOOK_NAMES.get(book_prefix, "Unknown Book")
        return f"{book_name} {int(chapter_num)}"

    # For files like x08a01.htm, x25b01.htm (split books)
    match2 = re.match(r'x(\d{2})([ab])(\d{2})\.htm', filename)
    if match2:
        book_prefix = f"x{match2.group(1)}{match2.group(2)}"
        chapter_num = match2.group(3)
        book_name = BOOK_NAMES.get(book_prefix, "Unknown Book")
        return f"{book_name} {int(chapter_num)}"

    # For files like x26a0.htm, x26b0.htm (Psalms with single-digit chapters)
    match3 = re.match(r'x(\d{2})([a-f])(\d)\.htm', filename)
    if match3:
        book_prefix = f"x{match3.group(1)}{match3.group(2)}"
        chapter_num = match3.group(3)
        book_name = BOOK_NAMES.get(book_prefix, "Unknown Book")
        return f"{book_name}{int(chapter_num)}"

    return "Unknown Book"


def process_all_files(directory):
    """Process all relevant Bible files to create plain text Bible files."""
    # Define patterns to match all chapter files
    patterns = [
        os.path.join(directory, "x[0-9][0-9][0-9][0-9].htm"),  # For x0101.htm, x0102.htm, etc.
        os.path.join(directory, "x[0-9][0-9][a-b][0-9][0-9].htm"),  # For x08a01.htm, x25b01.htm, etc.
        os.path.join(directory, "x26[a-f][0-9].htm")  # For Psalms x26a1.htm, x26b2.htm, etc.
    ]

    all_files = []
    for pattern in patterns:
        all_files.extend(glob.glob(pattern))

    # Filter out files that are not chapters of books
    # Skip x51.htm through x55.htm and similar
    valid_files = []
    for file_path in all_files:
        base_name = os.path.basename(file_path)
        if not re.match(r'x5[1-5]\.htm', base_name):  # Skip unknown books
            valid_files.append(file_path)

    # Create a sorting key function that properly orders the files
    def get_sort_key(file_path):
        filename = os.path.basename(file_path)

        # For x0101.htm format
        match1 = re.match(r'x(\d{2})(\d{2})\.htm', filename)
        if match1:
            book_num = int(match1.group(1))
            chapter_num = int(match1.group(2))
            return (book_num, 0, chapter_num)  # 0 for non-split books

        # For x08a01.htm, x25b01.htm format
        match2 = re.match(r'x(\d{2})([ab])(\d{2})\.htm', filename)
        if match2:
            book_num = int(match2.group(1))
            part = 1 if match2.group(2) == 'a' else 2  # 1 for 'a', 2 for 'b'
            chapter_num = int(match2.group(3))
            return (book_num, part, chapter_num)

        # For x26a0.htm, x26b0.htm format (Psalms)
        match3 = re.match(r'x(\d{2})([a-f])(\d+)\.htm', filename)
        if match3:
            book_num = int(match3.group(1))
            part_letter = match3.group(2)
            part = ord(part_letter) - ord('a') + 1  # 'a'=1, 'b'=2, etc.
            chapter_num = int(match3.group(3))
            return (book_num, part, chapter_num)

        # Default case
        return (99, 99, 99)  # Put unmatched files at the end

    # Sort the files
    valid_files.sort(key=get_sort_key)

    # Create the output files
    with codecs.open("TextFiles/bible_full.txt", 'w', 'utf-8') as full_file, \
            codecs.open("TextFiles/bible_hesher.txt", 'w', 'utf-8') as hesher_file:

        for file_path in valid_files:
            # Extract base name for logging and book/chapter identification
            base_name = os.path.basename(file_path)
            book_chapter = get_book_and_chapter(base_name)
            print(f"Processing {base_name} ({book_chapter})...")

            # Extract text from the HTML file
            text = extract_text_from_html(file_path)

            # Process for the full version
            full_text = process_full_text(text)
            full_text = clean_text(full_text)

            # Process for the hesher version
            hesher_text = process_hesher_text(text)
            hesher_text = clean_text(hesher_text)

            # Skip writing empty content
            if not full_text.strip() or not hesher_text.strip():
                print(f"Warning: Empty content in {base_name}, skipping...")
                continue

            # Write to the output files with book and chapter info
            full_file.write(f"{book_chapter}\n\n")
            full_file.write(full_text)
            full_file.write("\n\n")

            hesher_file.write(f"{book_chapter}\n\n")
            hesher_file.write(hesher_text)
            hesher_file.write("\n\n")

    print("Done! Bible text has been extracted to bible_full.txt and bible_hesher.txt")


if __name__ == "__main__":
    # Change this to the directory containing your HTML files
    html_directory = "MechonMamre"  # Current directory
    process_all_files(html_directory)