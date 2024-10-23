import json
import csv
from datetime import datetime
import sys
import os
from pathlib import Path

def sanitize_filename(filename):
    """
    Convert a string to a valid filename by removing or replacing invalid characters.
    
    Args:
        filename (str): The string to convert to a valid filename
    
    Returns:
        str: A valid filename
    """
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    # Remove any leading/trailing spaces and periods
    filename = filename.strip('. ')
    return filename

def convert_trello_to_csv(input_file, output_file=None):
    """
    Convert Trello JSON export to CSV format.
    
    Args:
        input_file (str): Path to Trello JSON export file
        output_file (str, optional): Path to output CSV file. If None, uses board name
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    # Read JSON file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            trello_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return False
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON file: {input_file}")
        return False

    # If no output file specified, use board name
    if output_file is None:
        board_name = trello_data.get('name', 'trello_export')
        safe_board_name = sanitize_filename(board_name)
        output_dir = os.path.dirname(input_file)
        output_file = os.path.join(output_dir, f"{safe_board_name}.csv")
        
        # Ensure we don't overwrite existing files
        base_name = os.path.splitext(output_file)[0]
        counter = 1
        while os.path.exists(output_file):
            output_file = f"{base_name}_{counter}.csv"
            counter += 1
    
    # Create a lookup dictionary for lists by ID
    lists_dict = {lst['id']: lst['name'] for lst in trello_data.get('lists', [])}
    
    # Create a lookup dictionary for members by ID
    members_dict = {member['id']: member.get('email', member.get('username', '')) 
                   for member in trello_data.get('members', [])}

    # Prepare CSV data
    csv_data = []
    
    # Process cards
    for card in trello_data.get('cards', []):
        # Get assigned members' emails/usernames
        assigned_to = '; '.join(members_dict.get(member_id, '')
                              for member_id in card.get('idMembers', []))
        
        # Get labels
        labels = '; '.join(label.get('name', '') 
                          for label in card.get('labels', []))
        
        # Format dates
        start_date = ''
        if 'start' in card:
            try:
                start_date = datetime.fromisoformat(card['start'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
            except (ValueError, AttributeError):
                pass

        due_date = ''
        if card.get('due'):
            try:
                due_date = datetime.fromisoformat(card['due'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
            except (ValueError, AttributeError):
                pass

        # Create row
        row = {
            'Title': card.get('name', ''),
            'List (Bucket)': lists_dict.get(card.get('idList', ''), ''),
            'Description': card.get('desc', ''),
            'Start Date': start_date,
            'Due Date': due_date,
            'Assigned To': assigned_to,
            'Labels': labels
        }
        
        csv_data.append(row)

    # Write to CSV
    if csv_data:
        fieldnames = ['Title', 'List (Bucket)', 'Description', 'Start Date', 
                     'Due Date', 'Assigned To', 'Labels']
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
            print(f"Successfully converted to CSV: {output_file}")
            return True
        except PermissionError:
            print(f"Error: Permission denied when writing to '{output_file}'")
            return False
        except Exception as e:
            print(f"Error writing CSV file: {str(e)}")
            return False
    else:
        print(f"No card data found in the JSON file: {input_file}")
        return False

def process_input(input_path, output_path=None):
    """
    Process either a single JSON file or all JSON files in a directory.
    
    Args:
        input_path (str): Path to input file or directory
        output_path (str, optional): Path to output file or directory
    """
    input_path = Path(input_path)
    
    if input_path.is_file():
        # Process single file
        if output_path:
            convert_trello_to_csv(str(input_path), output_path)
        else:
            convert_trello_to_csv(str(input_path))
    
    elif input_path.is_dir():
        # Process all JSON files in directory
        json_files = list(input_path.glob('*.json'))
        
        if not json_files:
            print(f"No JSON files found in directory: {input_path}")
            return
        
        successful_conversions = 0
        for json_file in json_files:
            if output_path:
                # If output_path is specified and is a directory, create CSV there
                if os.path.isdir(output_path):
                    output_file = os.path.join(output_path, f"{json_file.stem}.csv")
                else:
                    print(f"Error: Output path '{output_path}' is not a directory")
                    return
            else:
                output_file = None
            
            if convert_trello_to_csv(str(json_file), output_file):
                successful_conversions += 1
        
        print(f"\nProcessed {len(json_files)} JSON files with {successful_conversions} successful conversions")
    
    else:
        print(f"Error: Input path '{input_path}' does not exist")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # Use only input path, output will be based on board name
        process_input(sys.argv[1])
    elif len(sys.argv) == 3:
        # Use both input and output paths
        process_input(sys.argv[1], sys.argv[2])
    else:
        print("Usage:")
        print("  python script.py <input_path>")
        print("  python script.py <input_path> <output_path>")
        print("\nWhere:")
        print("  <input_path> can be a JSON file or a directory containing JSON files")
        print("  <output_path> (optional) can be a CSV file (for single file input)")
        print("                           or a directory (for directory input)")
        sys.exit(1)