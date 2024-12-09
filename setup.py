from setuptools import setup, find_packages

with open("README.md", 'r') as file:
    long_description = file.read()

setup(
    name="fs-search",
    version="0.1.0.1",
    description="CLI tool for listing paths in the base directory",
    author="voyager-2021",
    author_email="voyager-2019@outlook.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": [
            "mypy>=1.13.0",
            "setuptools>=75.6.0",
            "twine>=6.0.1"
        ],
    },
    python_requires=">=3.10,<4.0",
    entry_points={
        "console_scripts": [
            "fs-search = fs_search.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/voyager-2021/fs-search",
    project_urls={
        "Source": "https://github.com/voyager-2021/fs-search",
        "Issues": "https://github.com/voyager-2021/fs-search/issues",
    },
    long_description=long_description,
    long_description_content_type="text/markdown"
)
