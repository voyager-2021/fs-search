import argparse
import os

def update_setup_py(filepath, package, target, action):
    if not os.path.exists(filepath):
        print(f"Error: The file {filepath} does not exist.")
        return

    with open(filepath, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    in_target_section = False
    package_added_or_removed = False

    for line in lines:
        stripped = line.strip()

        # Detect target section
        if target == "requires" and stripped.startswith("install_requires"):
            in_target_section = True
        elif target == "dev" and stripped.startswith('"dev": ['):
            in_target_section = True

        # Process lines within the target section
        if in_target_section and stripped.endswith('['):  # Start of list
            updated_lines.append(line)
            if action == "add":
                updated_lines.append(f'        "{package}",\n')
                package_added_or_removed = True
            in_target_section = False  # Ensure we only modify once
        elif in_target_section and action == "remove" and f'"{package}"' in stripped:
            # Skip the line containing the package to be removed
            package_added_or_removed = True
            continue
        else:
            updated_lines.append(line)

    if action == "add" and not package_added_or_removed:
        print(f"Warning: Could not find target section '{target}' to add the package.")
    elif action == "remove" and not package_added_or_removed:
        print(f"Warning: Package '{package}' not found in target section '{target}'.")

    # Write updated lines back to the file
    with open(filepath, 'w') as file:
        file.writelines(updated_lines)

    print(f"Successfully {action}ed '{package}' in {target} section of {filepath}.")

def main():
    parser = argparse.ArgumentParser(description="Manage dependencies in setup.py.")
    parser.add_argument(
        "action",
        choices=["add", "remove"],
        help="Action to perform: add or remove a package.",
    )
    parser.add_argument(
        "--target", "-t", 
        choices=["requires", "dev"],
        required=False,
        help="The target section to update (requires or dev).",
        default="requires",
    )
    parser.add_argument(
        "--package", "-p",
        required=True,
        help="The package name to add or remove.",
    )
    parser.add_argument(
        "--file", "-f",
        default="setup.py",
        help="The path to the setup.py file (default: setup.py).",
        required=False,
    )

    args = parser.parse_args()
    update_setup_py(args.file, args.package, args.target, args.action)

if __name__ == "__main__":
    main()
