from .suitable import find_most_relevant_keyword
import argparse
import pathlib
import os
import logging
from tqdm import tqdm

directories = []


logging.basicConfig(level=logging.ERROR, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str, help="path of the directory to sort")
args = parser.parse_args()

directory_path = pathlib.Path(args.path)
if not directory_path.exists():
    logger.error("Directory was not found.")
    exit(0)

file_paths = [str(file_path) for file_path in directory_path.iterdir() if file_path.is_file()]

progress_bar = tqdm(file_paths, desc="Processing files", unit="file(s)", dynamic_ncols=True)

for file in progress_bar:
    if not file.endswith('.txt'):
        progress_bar.write(f"Skipping file {file} because it is not a .txt file.")
        continue
    
    try:
        with open(file, 'r') as f:
            keyword = find_most_relevant_keyword(f.read(), directories)
            if keyword is None:
                continue

        new_directory_path = directory_path / keyword
        new_directory_path.mkdir(parents=True, exist_ok=True)
        new_file_path = new_directory_path / pathlib.Path(file).name
        os.rename(file, new_file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file}")
    except IsADirectoryError:
        logger.error(f"Expected a file but found a directory: {file}")
    except UnicodeDecodeError:
        logger.error(f"Unable to decode file: {file}")
    except PermissionError:
        logger.error(f"Permission denied: {file}")

progress_bar.close()
