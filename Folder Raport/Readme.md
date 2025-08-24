# Folder Report

A Python program that analyzes the contents of a given folder and generates a detailed, readable report in the terminal. It provides:

- The total number of files and folders.
- A count and size breakdown of **Images** and **Videos**.
- A ranked list of subfolders based on their total size.

## Features

- **Folder Size Calculation**: Computes the size of each subfolder.
- **File Type Breakdown**: Only tracks **Images** and **Videos**.
- **Subfolder Sorting**: Ranks subfolders from the largest to the smallest based on their size.

## Requirements

You need to install the `rich` library for formatted terminal output:

```bash
pip install rich
