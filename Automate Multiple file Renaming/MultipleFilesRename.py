
import os
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def rename_files_in_directory(directory_path, delimiter='-', ignore_files=None):
    """
    Renames files in a given directory based on a specific naming pattern.
    
    Parameters:
    directory_path (str): The path to the directory containing the files to rename.
    delimiter (str): The character used to split parts of the filenames (default is '-').
    ignore_files (list): A list of filenames to ignore during processing (default is ['.DS_Store']).
    
    The function expects filenames in the format: Title-Course-Number.ext
    It renames files to: Number-Title-Course.ext with zero-padded numbers.
    """
    
    if ignore_files is None:
        ignore_files = ['.DS_Store']  # Default files to ignore, like the .DS_Store on macOS

    max_num_len = 0  # Variable to track the length of the largest number in filenames
    files_info = []  # List to store tuples of (filename, parts, extension)

    # First pass: Gather file info and determine max_num_len for zero-padding
    for f in os.listdir(directory_path):
        if f in ignore_files:
            continue  # Skip ignored files

        file_name, file_ext = os.path.splitext(f)
        try:
            parts = file_name.split(delimiter)  # Split filename into parts based on delimiter
            if len(parts) != 3:  # Check if filename has the expected number of parts
                logging.warning(f"Skipping file due to unexpected format: {f}")
                continue

            f_number = parts[2].strip()  # Assuming the number is the third part
            if f_number.isdigit():
                max_num_len = max(max_num_len, len(f_number))  # Update max number length if needed
            files_info.append((f, parts, file_ext))  # Store file info for later processing
        except Exception as e:
            logging.error(f"Error processing file '{f}': {e}")
            continue

    # Second pass: Rename files based on the gathered info
    for f, parts, file_ext in files_info:
        f_title = parts[0].strip()  # Extract and strip the title part
        f_course = parts[1].strip()  # Extract and strip the course part
        f_number = parts[2].strip()  # Extract and strip the number part

        if f_number.isdigit():
            f_number = f_number.zfill(max_num_len)  # Zero-pad the number based on max length

        # Construct the new filename in the format: Number-Title-Course.ext
        new_name = f'{f_number}{delimiter}{f_title}{delimiter}{f_course}{file_ext}'
        
        # Form full paths for renaming
        old_path = os.path.join(directory_path, f)
        new_path = os.path.join(directory_path, new_name)

        try:
            os.rename(old_path, new_path)  # Rename the file
            logging.info(f"Renamed '{f}' to '{new_name}'")
        except Exception as e:
            logging.error(f"Error renaming file '{f}' to '{new_name}': {e}")

# Example Usage:
# Suppose we have a directory at '/path/to/files/' with the following files:
# 1. 'Introduction-Python-3.txt'
# 2. 'Advanced-Python-10.txt'
# 3. 'Basics-Java-2.txt'

directory_path = '/Users/antar/OneDrive/Belgeler/files'
rename_files_in_directory(directory_path)

# After running the script, the files will be renamed to:
# 1. '03-Introduction-Python.txt'
# 2. '10-Advanced-Python.txt'
# 3. '02-Basics-Java.txt'

# Note: The number part is zero-padded based on the largest number (in this case, '10').
