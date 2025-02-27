import argparse
import os
import re
import tabulate

def search_files_by_pattern(root_dir, pattern):
    matched_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if re.search(pattern, file):
                matched_files.append(os.path.join(root, file))
    return matched_files

def search_text_in_files(files, search_text):
    results = []
    for file in files:
        with open(file, 'r') as f:
            content = f.read()
            if search_text in content:
                file_attributes = os.stat(file)
                results.append({
                    'file_name': os.path.basename(file),
                    'file_path': file,
                    'file_attributes': file_attributes
                })
    return results

def main():
    parser = argparse.ArgumentParser(description='Search for files by pattern and look for user-defined text inside file contents.')
    parser.add_argument('pattern', type=str, help='Regexp pattern to search for in file names')
    parser.add_argument('search_text', type=str, help='Text to search for inside files')
    parser.add_argument('root_dir', type=str, nargs='?', default='.', help='Root directory to start the search (default: current directory)')
    args = parser.parse_args()

    matched_files = search_files_by_pattern(args.root_dir, args.pattern)
    results = search_text_in_files(matched_files, args.search_text)

    table = []
    for result in results:
        table.append([result['file_name'], result['file_path'], result['file_attributes']])
    print(tabulate.tabulate(table, headers=['File Name', 'File Path', 'File Attributes'], tablefmt='grid'))

if __name__ == '__main__':
    main()
  
