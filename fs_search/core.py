from colorama import Fore, Style, init
from pathlib import Path
from typing import List
import sys
import os

# Initialize colorama
init(autoreset=True)

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
        extension = f".{extension}"
    return extension


def search_files_and_dirs(
    base_path: Path,
    exclude_exts: List[str],
    exclude_dirs: List[str],
    files_only: bool,
    folders_only: bool,
) -> List[str]:
    """Search files and directories, excluding certain extensions and directories."""
    results = []


    try:
        for root_, dirs, files in os.walk(base_path):

            root = Path(root_)

            # Exclude directories if any match
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            if not folders_only:
                for file in files:
                    file_path = root / file  # Use / operator to join paths (cross-platform)
                    if not any(file_path.suffix == ext for ext in exclude_exts):
                        results.append(str(file_path))  # Convert Path to string

            if not files_only:
                for dir in dirs:
                    dir_path = root / dir
                    results.append(str(dir_path))

    except Exception as e:
        print(f"{Fore.RED}Error while searching: {e}")
        sys.exit(1)

    return results


def save_results(output_file: str, results: List[str]) -> None:
    """Save results to a file."""
    try:
        with open(output_file, "w") as f:
            f.writelines(f"{line}\n" for line in results)
        print(f"{Fore.MAGENTA}Total found: {len(results)}")
        print(f"{Fore.GREEN}Results written to {output_file}")
    except Exception as e:
        print(f"{Fore.RED}Error writing to file: {e}")
        sys.exit(1)


def display_results(results: List[str]) -> None:
    """Display results in the console."""
    for result in results:
        print(f"{Fore.CYAN}{result}")
    print(f"{Fore.MAGENTA}Total found: {len(results)}")
