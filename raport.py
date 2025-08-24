import os
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

# Define file type categories
IMAGE_EXTS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
VIDEO_EXTS = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv']

def get_size_readable(size_bytes):
    """Convert size in bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"

def calculate_folder_size(path):
    """Calculate the total size of a folder including subfolders."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            total_size += os.path.getsize(os.path.join(dirpath, file))
    return total_size

def analyze_folder(path):
    summary = {
        "folders": 0,
        "total_files": 0,
        "images": {"count": 0, "size": 0},
        "videos": {"count": 0, "size": 0},
    }

    subfolder_reports = []

    for root, dirs, files in os.walk(path):
        folder_name = os.path.relpath(root, path)
        folder_size = calculate_folder_size(root)

        folder_data = {
            "folder": folder_name,
            "size": folder_size,
            "images": {"count": 0, "size": 0},
            "videos": {"count": 0, "size": 0},
            "files": len(files)
        }

        summary["folders"] += len(dirs)
        summary["total_files"] += len(files)

        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            size = os.path.getsize(file_path)

            if ext in IMAGE_EXTS:
                key = "images"
            elif ext in VIDEO_EXTS:
                key = "videos"
            else:
                continue  # Skip non-image/video files

            summary[key]["count"] += 1
            summary[key]["size"] += size

            folder_data[key]["count"] += 1
            folder_data[key]["size"] += size

        subfolder_reports.append(folder_data)

    # Sort subfolders by size in descending order (biggest to smallest)
    subfolder_reports.sort(key=lambda x: x["size"], reverse=True)

    return summary, subfolder_reports

def print_report(summary, subfolders):
    console.rule("[bold green]📊 Folder Analysis Summary")

    table = Table(title="📁 Folder Summary Report", show_lines=True)

    table.add_column("Type", justify="left", style="cyan", no_wrap=True)
    table.add_column("Count", justify="right", style="magenta")
    table.add_column("Size", justify="right", style="green")

    table.add_row("Images", str(summary["images"]["count"]), get_size_readable(summary["images"]["size"]))
    table.add_row("Videos", str(summary["videos"]["count"]), get_size_readable(summary["videos"]["size"]))
    table.add_row("Total Files", str(summary["total_files"]), "-")
    table.add_row("Total Folders", str(summary["folders"]), "-")

    console.print(table)

    console.rule("[bold blue]📂 Subfolder Breakdown (Biggest to Smallest)")

    folder_table = Table(show_lines=True)
    folder_table.add_column("Subfolder", style="cyan")
    folder_table.add_column("Files", justify="right")
    folder_table.add_column("Folder Size", justify="right")
    folder_table.add_column("Images", justify="right")
    folder_table.add_column("Videos", justify="right")

    for data in subfolders:
        folder_table.add_row(
            data["folder"],
            str(data["files"]),
            get_size_readable(data["size"]),
            f'{data["images"]["count"]} ({get_size_readable(data["images"]["size"])})',
            f'{data["videos"]["count"]} ({get_size_readable(data["videos"]["size"])})'
        )

    console.print(folder_table)

def main():
    folder_path = input("📁 Enter the folder path to analyze: ").strip()
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        console.print("[red]❌ Invalid folder path. Please try again.")
        return

    console.print(f"[bold yellow]Analyzing folder:[/bold yellow] {folder_path}\n")
    summary, subfolders = analyze_folder(folder_path)
    print_report(summary, subfolders)

if __name__ == "__main__":
    main()
