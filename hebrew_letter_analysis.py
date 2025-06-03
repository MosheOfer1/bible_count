import csv
import collections

def count_hebrew_letters(file_path):
    """
    Reads a text file and counts each Hebrew letter's occurrence.
    
    Args:
        file_path (str): Path to the text file containing Hebrew text
        
    Returns:
        collections.Counter: Counter with Hebrew letters and their counts
    """
    # Hebrew Unicode range
    def is_hebrew_letter(char):
        return '\u0590' <= char <= '\u05FF'
    
    letter_counts = collections.Counter()
    total_letters = 0
    
    try:
        # Open and read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Count each Hebrew letter
            for char in content:
                if is_hebrew_letter(char):
                    letter_counts[char] += 1
                    total_letters += 1
            
            print(f"Counted {total_letters} Hebrew letters in total.")
            
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return letter_counts, total_letters

def export_letter_counts_to_csv(letter_counts, total_letters, output_file):
    """
    Exports Hebrew letter counts to a CSV file.
    
    Args:
        letter_counts (collections.Counter): Counter with Hebrew letters and their counts
        total_letters (int): Total number of Hebrew letters counted
        output_file (str): Path to the output CSV file
    """
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            # Create CSV writer
            csv_writer = csv.writer(csvfile)
            
            # Write header row
            csv_writer.writerow(['Hebrew Letter', 'Count', 'Percentage'])
            
            # Sort letters by count (descending)
            sorted_letters = letter_counts.most_common()
            
            # Write each letter's statistics
            for letter, count in sorted_letters:
                percentage = (count / total_letters) * 100
                csv_writer.writerow([letter, count, f"{percentage:.2f}%"])
            
            # Add a total row
            csv_writer.writerow(['Total', total_letters, '100.00%'])
        
        print(f"Successfully exported letter statistics to '{output_file}'")
        
    except Exception as e:
        print(f"Error exporting to CSV: {e}")

def print_letter_stats_table(letter_counts, total_letters):
    """
    Prints a table with Hebrew letter statistics.
    
    Args:
        letter_counts (collections.Counter): Counter with Hebrew letters and their counts
        total_letters (int): Total number of Hebrew letters counted
    """
    # Print table header
    print("\nHebrew Letter Statistics:")
    print("-" * 50)
    print(f"{'Letter':<10} | {'Count':<10} | {'Percentage':<10}")
    print("-" * 50)
    
    # Sort letters by count (descending)
    sorted_letters = letter_counts.most_common()
    
    # Print each letter's statistics
    for letter, count in sorted_letters:
        percentage = (count / total_letters) * 100
        print(f"{letter:<10} | {count:<10} | {percentage:.2f}%")
    
    # Print total
    print("-" * 50)
    print(f"{'Total':<10} | {total_letters:<10} | 100.00%")
    print("-" * 50)

if __name__ == "__main__":
    # File path for the Bible text
    file_path = "TextFiles/bible_full_v2_parshas.txt"
    
    # Count Hebrew letters
    letter_counts, total_letters = count_hebrew_letters(file_path)
    
    # Export to CSV
    output_csv = "hebrew_letter_counts.csv"
    export_letter_counts_to_csv(letter_counts, total_letters, output_csv)
    
    # Print statistics to console
    print_letter_stats_table(letter_counts, total_letters)