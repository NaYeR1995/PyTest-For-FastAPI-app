from pathlib import Path

def delete_pycache_folders(root_dir: str = '.'):
    """Recursively delete all __pycache__ folders in the given directory."""
    root_path = Path(root_dir)
    
    for pycache in root_path.rglob('__pycache__'):
        print(f"Deleting: {pycache}")
        try:
            # Delete all files in the __pycache__ folder first
            for file in pycache.glob('*'):
                file.unlink()
            # Then delete the folder itself
            pycache.rmdir()
        except Exception as e:
            print(f"Error deleting {pycache}: {e}")

# Usage - run from your project root
delete_pycache_folders()