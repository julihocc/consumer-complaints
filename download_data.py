
import kagglehub
import os
import shutil
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

def download_and_setup_data():
    """
    Downloads the 'dushyantv/consumer_complaints' dataset using kagglehub.
    If 'CONSUMER_COMPLAINTS_PATH' environment variable is set, it moves/copies 
    the data to that location.
    Prints the final path where the data is located.
    """
    print("Downloading dataset 'dushyantv/consumer_complaints'...")
    # Download latest version
    try:
        downloaded_path = kagglehub.dataset_download("dushyantv/consumer_complaints")
        print(f"Dataset downloaded to cache: {downloaded_path}")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        sys.exit(1)

    target_env_var = "CONSUMER_COMPLAINTS_PATH"
    target_path_str = os.environ.get(target_env_var)

    if target_path_str:
        target_path = Path(target_path_str).resolve()
        print(f"'{target_env_var}' is set to: {target_path}")
        
        if not target_path.exists():
            print(f"Creating directory: {target_path}")
            target_path.mkdir(parents=True, exist_ok=True)
            
        print(f"Copying files from {downloaded_path} to {target_path}...")
        try:
            # We iterate and copy files to the target directory
            # If downloaded_path is a directory (which it usually is for kagglehub)
            source_dir = Path(downloaded_path)
            if source_dir.is_dir():
                for item in source_dir.iterdir():
                    dest = target_path / item.name
                    if dest.exists():
                         print(f"File {dest} already exists. Skipping copy.")
                    else:
                        if item.is_dir():
                             shutil.copytree(item, dest)
                        else:
                             shutil.copy2(item, dest)
                print(f"Data successfully setup at: {target_path}")
            else:
                # Fallback if for some reason it's a file, though unexpected for this dataset
                shutil.copy2(source_dir, target_path)
                print(f"Data successfully setup at: {target_path}")
        except Exception as e:
            print(f"Error moving/copying data: {e}")
            print(f"Review the files at the original cache: {downloaded_path}")
            sys.exit(1)
    else:
        print(f"'{target_env_var}' environment variable is not set.")
        print(f"Data remains in cache: {downloaded_path}")
        print(f"To use a specific folder, set '{target_env_var}' and run this script again.")

if __name__ == "__main__":
    download_and_setup_data()
