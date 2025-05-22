import csv  # Add this import at the top of your file


def find_and_process_ampersand_words(file_path):
    """
    Reads a text file, finds words with '&', splits them at '&',
    and removes non-Hebrew characters.

    Args:
        file_path (str): Path to the text file to be processed

    Returns:
        list: List of processed Hebrew text parts
    """
    parsha_names = []
    processed_hebrew_parts = {}

    # Hebrew Unicode range (1400-05FF for Hebrew and some related symbols)
    def is_hebrew_char(char):
        # Hebrew Unicode range
        return char == " " or '\u0590' <= char <= '\u05FF'

    try:
        # Open and read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the entire content and split into words
            content = file.read()
            parts = content.split("&")[1:]

            # Take only the Torah part, before Joshua
            parts[-1] = parts[-1][:parts[-1].find("Joshua")]
            parsha_names = [parts[i][:min(parts[i].find(" "), parts[i].find("\n"))] for i in range(len(parts))]

            for index1, part in enumerate(parts):
                # Filter to keep only Hebrew characters
                parsha = ''.join(char for char in part if is_hebrew_char(char))

                # Add non-empty parts to the result list
                if parsha:
                    processed_hebrew_parts[parsha_names[index1]] = parsha

            print(f"Processed {len(processed_hebrew_parts)} Hebrew parts.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return parsha_names, processed_hebrew_parts


def export_parsha_stats_to_csv(hebrew_parts, output_file):
    """
    Exports Parsha statistics (name, word count, letter count) to a CSV file.

    Args:
        hebrew_parts (dict): Dictionary with Parsha name as key and Hebrew text as value
        output_file (str): Path to the output CSV file
    """
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            # Create CSV writer
            csv_writer = csv.writer(csvfile)

            # Write header row
            csv_writer.writerow(['Parsha Name', 'Words', 'Letters'])

            # Calculate and write statistics for each Parsha
            for parsha_name, text in hebrew_parts.items():
                # Count words (split by spaces)
                words = [word for word in text.split() if word.strip()]
                word_count = len(words)

                # Count letters (excluding spaces)
                letter_count = sum(1 for char in text if char != ' ')

                # Write row to CSV
                csv_writer.writerow([parsha_name, word_count, letter_count])

        print(f"Successfully exported Parsha statistics to '{output_file}'")

    except Exception as e:
        print(f"Error exporting to CSV: {e}")


def print_parsha_stats_table(hebrew_parts):
    """
    Prints a table with Parsha name, word count, and letter count.

    Args:
        hebrew_parts (dict): Dictionary with Parsha name as key and Hebrew text as value
    """
    # Print table header
    print("\nParsha Statistics:")
    print("-" * 60)
    print(f"{'Parsha Name':<20} | {'Words':<10} | {'Letters':<10}")
    print("-" * 60)

    # Calculate and print statistics for each Parsha
    for parsha_name, text in hebrew_parts.items():
        # Count words (split by spaces)
        words = [word for word in text.split() if word.strip()]
        word_count = len(words)

        # Count letters (excluding spaces)
        letter_count = sum(1 for char in text if char != ' ')

        # Print row
        print(f"{parsha_name:<20} | {word_count:<10} | {letter_count:<10}")

    print("-" * 60)


if __name__ == "__main__":
    # Get the file path from user input
    file_path = "TextFiles/תנ'ך עם חלוקת פרקים וסימון פרשיות - על פי מכון ממרא.txt"

    # Find words with ampersand and process them
    original_words, hebrew_parts = find_and_process_ampersand_words(file_path)

    # Export to CSV
    output_csv = "parsha_statistics.csv"
    export_parsha_stats_to_csv(hebrew_parts, output_csv)

    # Optionally, still print the table to console
    print_parsha_stats_table(hebrew_parts)