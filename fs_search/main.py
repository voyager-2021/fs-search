import argparse
from fs_search.core import (
    validate_base_path,
    validate_extension,
    search_files_and_dirs,
    save_results,
    display_results,
)
from pathlib import Path
from colorama import Fore, Style


def main() -> None:
    """Entry point of the CLI tool."""
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

    args = parser.parse_args()

    # Validate base path
    base_path = validate_base_path(args.base_path)

    # Validate extensions
    exclude_exts = [validate_extension(ext) for ext in args.exclude]

    # Validate directories to exclude
    exclude_dirs = [dir for dir in args.exclude_dirs]

    # Check conflicting options
    if args.files_only and args.folders_only:
        print(
            f"{Fore.RED}Error: You cannot use --files-only and --folders-only together."
        )
        return

    # Perform the search
    print(f"{Fore.BLUE}Searching in: {base_path}")
    results = search_files_and_dirs(
        base_path=base_path,
        exclude_exts=exclude_exts,
        exclude_dirs=exclude_dirs,
        files_only=args.files_only,
        folders_only=args.folders_only,
    )

    if args.relative:
        base_path = Path(base_path).resolve()
        results = [str(Path(result).relative_to(base_path)) for result in results]

    # Output results
    if args.output_file:
        save_results(args.output_file, results)
    else:
        display_results(results)

    print(f"{Fore.GREEN}Search completed!")


if __name__ == "__main__":
    main()
