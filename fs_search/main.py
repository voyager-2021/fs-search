import argparse
from fs_search.core import (
    validate_base_path,
    validate_extension,
    search_files_and_dirs,
    save_results,
    display_results,
)
from pathlib import Path
import time
import sys

def get_time(func, precision: int):
    start = time.perf_counter()
    func()
    end = time.perf_counter()
    total = round(end - start, precision)
    print(f'{func.__name__}() Took {total} seconds to run')


def main() -> None:
    """Entry point of the CLI tool."""
    try:
        from colorama import Fore, Style, init
        init(autoreset=True)  # Initializes colorama
    except ImportError:
        print("colorama module not found. Install it using 'pip install colorama'.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Search files and directories.")
    parser.add_argument(
        "-b", "--base-path", type=str, default=".", help="Base path to start the search."
    )
    parser.add_argument(
        "-e", "--exclude", action="append", default=[], help="File extensions to exclude (e.g., .log)."
    )
    parser.add_argument(
        "-E", "--exclude-dirs", action="append", default=[], help="Directories to exclude (e.g., node_modules)."
    )
    parser.add_argument(
        "-f", "--files-only", action="store_true", help="Search only files."
    )
    parser.add_argument(
        "-d", "--folders-only", action="store_true", help="Search only folders."
    )
    parser.add_argument(
        "-o", "--output-file", type=str, help="File to save the results."
    )
    parser.add_argument(
        "-r", "--relative", action="store_true", help="Display relative paths instead of full paths."
    )
    parser.add_argument(
        "-t", "--time", action="store_true", help="Times the search."
    )

    args = parser.parse_args()

    # Validate base path
    try:
        base_path = validate_base_path(args.base_path)
    except ValueError as e:
        print(f"{Fore.RED}Error: {e}")
        return

    # Validate extensions
    exclude_exts = [validate_extension(ext) for ext in args.exclude]

    # Validate directories to exclude
    exclude_dirs = [dir for dir in args.exclude_dirs]

    # Check conflicting options
    if args.files_only and args.folders_only:
        print(f"{Fore.RED}Error: You cannot use --files-only and --folders-only together.")
        return

    print(f"{Fore.BLUE}Searching in: {base_path}")

    if args.time:
        start = time.perf_counter()

    # Perform the search
    results = search_files_and_dirs(
        base_path=base_path,
        exclude_exts=exclude_exts,
        exclude_dirs=exclude_dirs,
        files_only=args.files_only,
        folders_only=args.folders_only,
    )

    if args.time:
        end = time.perf_counter()
        total = end - start

    if not results:
        print(f"{Fore.YELLOW}No results found.")
        return

    if args.relative:
        base_path = Path(base_path).resolve()
        results = [str(Path(result).relative_to(base_path)) for result in results]

    # Output results
    if args.output_file:
        save_results(args.output_file, results)
    else:
        display_results(results)

    print(f"{Fore.GREEN}Search completed!")
    
    if args.time:
        print(f"{Fore.LIGHTCYAN_EX}Took {total:.8f} seconds.")



if __name__ == "__main__":
    main()
