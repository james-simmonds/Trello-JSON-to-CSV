# Trello JSON to CSV Converter

A Python script that converts Trello board exports (JSON format) to CSV files. The script can process either individual JSON files or entire directories containing multiple Trello board exports.

## Features

- Converts Trello cards to CSV format with essential fields
- Automatically names output files based on board names
- Supports batch processing of multiple JSON files
- Handles file naming conflicts automatically
- Preserves UTF-8 encoding for special characters
- Maintains data relationships (lists, members, labels)

## CSV Output Format

The generated CSV files include the following columns:
- Title (Card name)
- List (Bucket) (List/column name)
- Description
- Start Date
- Due Date
- Assigned To (Members)
- Labels

## Prerequisites

- Python 3.6 or higher
- No additional packages required (uses only Python standard library)

## Installation

1. Download both script files:
   - `trello_to_csv.py`

2. Ensure you have Python 3.6 or higher installed:
   ```bash
   python --version
   ```

## Usage

### Single File Processing

To convert a single Trello JSON export, using board name for output filename:
```bash
python trello_to_csv.py input.json
```

To convert a single file with a custom output filename:
```bash
python trello_to_csv.py input.json output.csv
```

### Batch Processing

To convert all JSON files in a directory, saving CSVs in the same directory:
```bash
python trello_to_csv.py /path/to/input/folder
```

To convert all JSON files in a directory, saving CSVs in a specific output directory:
```bash
python trello_to_csv.py /path/to/input/folder /path/to/output/folder
```

## How to Export Trello Boards

1. Open your Trello board
2. Click 'Show Menu' (three dots) in the top right
3. Select 'More'
4. Choose 'Print and Export'
5. Click 'Export to JSON'
6. Save the downloaded file

## Error Handling

The script includes comprehensive error handling for:
- Missing input files
- Invalid JSON format
- Permission issues
- File naming conflicts
- Directory creation
- UTF-8 encoding issues

## Output File Naming

- When processing a single file without specifying an output name, the script uses the board name from the JSON file
- The script automatically handles naming conflicts by appending numbers (e.g., "Board_Name_1.csv")
- Invalid characters in board names are replaced with underscores
- When processing a directory, each output file is named after its corresponding input JSON file unless specified otherwise

## Example Output

```csv
Title,List (Bucket),Description,Start Date,Due Date,Assigned To,Labels
"Setup Docker","Development","Install Docker Desktop...","2024-01-15","2024-01-20","john.doe@email.com","Infrastructure; Setup"
"Update Guide","Documentation","Review and update...","2024-02-01","2024-02-15","jane.smith@email.com","Documentation"
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - feel free to use it in your own projects.