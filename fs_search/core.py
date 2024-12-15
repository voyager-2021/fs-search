from fs_search.utils import lru_cache
from colorama import Fore, init
from pathlib import Path
from typing import List
import hashlib
import json
import sys
import os


# Initialize colorama
init(autoreset=True)

CACHE_FILE = os.environ.get("FS_SEARCH_CACHE_FILE")

if CACHE_FILE is None:
    if os.name == "nt":
        CACHE_FILE = Path(f"{Path.home()}\\.fs_search")
    else:
        CACHE_FILE = os.environ.get("XDG_CACHE_HOME")
        if CACHE_FILE is None:
            CACHE_FILE = Path.home() / ".fs_search"
        else:
            CACHE_FILE = Path(os.environ.get("XDG_CACHE_HOME")) / ".fs_search"


def load_cache():
    """Load the cache from a file."""
    if not CACHE_FILE.exists():
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

def save_cache(cache):
    """Save the cache to a file."""
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file)

def generate_cache_key(base_path, exclude_exts, exclude_dirs, files_only, folders_only):
    """Generate a unique cache key based on search parameters."""
    key_data = f"{base_path}_{exclude_exts}_{exclude_dirs}_{files_only}_{folders_only}"
    return hashlib.sha256(key_data.encode()).hexdigest()

def validate_base_path(base_path_: str) -> Path:
    """Validate the base path and return it as a Path object."""
    base_path = Path(base_path_).resolve()  # Convert to absolute path
    if not base_path.exists():
        print(f"{Fore.RED}Error: Base path '{base_path}' does not exist.")
        sys.exit(1)
    return base_path

def validate_extension(extension: str) -> str:
    """Ensure the extension starts with a dot."""
    if not extension.startswith("."):
        extension = "." + extension
    return extension

def is_cache_valid(cache, key, base_path):
    """Check if the cache entry is still valid."""
    if key not in cache:
        return False
    cached_entry = cache[key]
    # Check if the directory's modification time matches
    current_mtime = os.path.getmtime(base_path)
    return cached_entry["mtime"] == current_mtime

def clear_cache() -> None:
    """Clear the disk cache and reinitialize it."""
    cache = load_cache()
    cache.clear()
    save_cache(cache)
    print(f"{Fore.YELLOW}Cache has been cleared and reinitialized...")

@lru_cache(10_000)
def search_files_and_dirs(
    base_path: Path,
    exclude_exts: List[str],
    exclude_dirs: List[str],
    files_only: bool,
    folders_only: bool,
    print_while_searching: bool = False,
    silent: bool = False,
    disable_caching: bool = False,
    remake_cache: bool = False
) -> List[str]:
    """Search files and directories, excluding certain extensions and directories."""
    if not disable_caching and not remake_cache:
        cache = load_cache()
        key = generate_cache_key(base_path, exclude_exts, exclude_dirs, files_only, folders_only)

        if is_cache_valid(cache, key, base_path):
            print(f"{Fore.GREEN}Using cached results...")
            return cache[key]["results"]

        print(f"{Fore.YELLOW}Performing fresh search...")

    if remake_cache:
        cache = load_cache()
        clear_cache()
        print(f"{Fore.YELLOW}Performing fresh search...")

    results = []

    current_dir = ""

    try:
        for root_, dirs, files in os.walk(base_path):

            root = Path(root_)

            # Exclude directories if any match
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            if not folders_only:
                for file in files:
                    file_path = root / file
                    if not any(file_path.suffix == ext for ext in exclude_exts):
                        results.append(str(file_path))
                    if not silent:
                        current_dir = str(file_path)

            if not files_only:
                for dir in dirs:
                    dir_path = root / dir
                    if not silent:
                        current_dir = str(dir_path)
                    results.append(str(dir_path))

            if print_while_searching and (not silent):
                print(f"{Fore.CYAN}{current_dir}")

    except Exception as e:
        print(f"{Fore.RED}Error while searching: {e}")
        sys.exit(1)

    if not disable_caching and not remake_cache:    
        cache[key] = {
            "mtime": os.path.getmtime(base_path),
            "results": results,
        }
        save_cache(cache)

    return results

def save_results(output_file: str, results: List[str]) -> None:
    """Save results to a file."""
    try:
        with open(output_file, "w", encoding="utf-32") as f:
            f.writelines(f"{line}\n" for line in results)
        print(f"{Fore.MAGENTA}Total found: {len(results)}")
        print(f"{Fore.GREEN}Results written to {output_file}")
    except Exception as e:
        print(f"{Fore.RED}Error writing to file: {e}")
        sys.exit(1)

def display_results(results: List[str], _silent: bool = False) -> None:
    """Display results in the console."""
    if not _silent:
        for result in results:
            print(f"{Fore.CYAN}{result}")
    print(f"{Fore.MAGENTA}Total found: {len(results)}")


