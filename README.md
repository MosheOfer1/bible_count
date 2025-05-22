# Bible Text Parser and Counter

This project parses Hebrew Bible text from HTML files provided by Mechon Mamre and performs word and letter counting.

## Attribution

The source text used in this project is the Hebrew Bible without vowels according to the Masoretic Text, provided by Mechon Mamre:

- © 2002 All rights reserved to Mechon Mamre for the HTML version
- Website: http://www.mechon-mamre.org/
- Contact: mtr@mechon-mamre.org

The Hebrew text is based on the Aleppo Codex and other early manuscripts using the method of Rav Mordechai Breuer. The original text conforms to the RaMBaM's Laws of Torah Scrolls Chapter 8's details on correct division of paragraphs.

## Project Components

### HTML Parser

The HTML parser extracts Bible text from Mechon Mamre HTML files and creates clean text versions:

1. **Input**: HTML files from Mechon Mamre with Bible text
2. **Processing**:
   - Extracts text content while preserving book and chapter structure
   - Removes verse numbers and special markers
   - Creates two versions:
     - **Full version**: Uses primary words when alternatives exist in parentheses
     - **Hesher version**: Uses alternative words found in parentheses
3. **Output**: Two clean text files with properly formatted Bible text

### Word and Letter Counter

The counter processes the parsed text files and generates statistics:

1. **Input**: Parsed Bible text with parsha (Torah portion) markers
2. **Processing**:
   - Splits text at parsha markers
   - Counts words and letters in each parsha
   - Filters text to include only Hebrew characters
3. **Output**:
   - CSV file with word and letter counts for each parsha
   - Console display of the same statistics in table format

## Usage

1. Place Mechon Mamre HTML Bible files in the `MechonMamre` directory
2. Run `html_parser.py` to generate clean text files
3. Run `words&letters_counter.py` to analyze and count words and letters

## License and Legal Notice

This project uses text from Mechon Mamre which is copyright protected. The parser and counter tools are for research and educational purposes only. Any redistribution of the processed text must maintain the original copyright notice and attribution to Mechon Mamre.