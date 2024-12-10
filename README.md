
# fs-search

`fs-search` is a command-line tool that allows you to search for files and directories within a specified base path. You can customize your search by including or excluding specific file extensions and directories, and the results can be displayed in a user-friendly format with options to save them to a file.

## Features

- Search for files and directories starting from a specified base path.
- Exclude files based on extensions (`-e`).
- Exclude directories from the search (`-E`).
- Search only for files (`-f`) or only for directories (`-d`).
- Save the results to a file (`-o`).
- Display relative paths instead of full paths (`-r`).
- Supports cross-platform usage with `pathlib`.
- Colorful output using `colorama`.
- Easily extendable for future features.

## Installation

You can install `fs-search` via pip:

```bash
pip install fs-search
```

## Usage

### Basic Search

Search the current directory for files and directories:

```bash
fs-search
```

### Exclude File Extensions

Exclude specific file extensions from the search:

```bash
fs-search -e .log -e .tmp
```

### Exclude Directories

Exclude specific directories from the search:

```bash
fs-search -E node_modules -E .git
```

### Search Only Files

Search only for files (excluding directories):

```bash
fs-search -f
```

### Search Only Directories

Search only for directories (excluding files):

```bash
fs-search -d
```

### Save Results to a File

Save the search results to a file:

```bash
fs-search -o results.txt
```

### Display Relative Paths

Display relative paths instead of full paths:

```bash
fs-search -r
```

### Combine Options

You can combine multiple options:

```bash
fs-search -b /path/to/search -e .log -E node_modules -f -o results.txt
```

## Development

To contribute to `fs-search`, you can clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/voyager-2021/fs-search.git
cd fs-search
pip install -e .[dev]
```

### Running Mypy

Run mypy before commiting. To run mypy (using `mypy`), simply run:

```bash
mypy search_fs --strict
```

### Todo
Optimize lol.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Links

- [GitHub Repository](https://github.com/voyager-2021/fs-search)
- [Bug Tracker](https://github.com/voyager-2021/fs-search/issues)
