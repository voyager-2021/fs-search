import argparse
import re

def bump_version(file_path, new_version):
    # Regex to handle flexible version patterns
    version_pattern = r'version\s*=\s*"(?:\d+\.\d+\.\d+(?:\.\d+)?(?:[ab]|(?:rc|alpha|beta|patch|hotfix)(?:-?\d+))?)"'
    updated = False

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Search and replace the version line
        for i in range(len(lines)):
            if re.search(version_pattern, lines[i]):
                lines[i] = re.sub(version_pattern, f'version="{new_version}"', lines[i])
                updated = True
                break

        if not updated:
            print("No version entry found in the file.")
            return

        with open(file_path, 'w') as file:
            file.writelines(lines)

        print(f"Version updated to {new_version} in {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Bump the version in a setup.py file.")
    parser.add_argument("file_path", help="Path to the setup.py file.")
    parser.add_argument("new_version", help="The new version string (e.g., X.X.Xrc1, X.X.Xa2, X.X.X.alpha-2).")
    
    args = parser.parse_args()
    bump_version(args.file_path, args.new_version)

if __name__ == "__main__":
    main()
