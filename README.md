# 🐍 Python Mini Projects

A collection of small yet useful Python projects.  
Each project is self-contained, beginner-friendly, and focuses on solving real-world problems.  
More projects will be added over time!

---

## 📋 Project List

| # | Project Name    | Description                                                                 | Status |
|---|-----------------|-----------------------------------------------------------------------------|--------|
| 1 | [Folder Report](#-folder-report) | Analyze a folder and generate a detailed report (files, folders, images, videos, sizes). | ✅ Done |
| 2 | _Coming Soon_   | More projects will be added gradually...                                   | ⏳ WIP |

---

## 📂 Folder Report

**Folder Report** is a Python program that analyzes the contents of a given folder and generates a detailed, human-readable report in the terminal.

### 🔑 Features
- **Folder Size Calculation** – Computes the size of each subfolder.  
- **File Type Breakdown** – Tracks **Images** and **Videos** (count + total size).  
- **Subfolder Sorting** – Ranks subfolders from largest to smallest.  
- **Formatted Output** – Uses [`rich`](https://github.com/Textualize/rich) for clean and colorful terminal tables.  

### 📦 Requirements
Install dependencies before running:

```bash
pip install rich
