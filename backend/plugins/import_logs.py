import os
from plugins.memory import add_memory

def batch_import(file_path, entry_type="unknown", split_marker="---"):
    """
    Import lines/sections from a file into ChromaDB.
    - Handles missing files gracefully
    - Skips empty entries
    - Logs progress
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return 0

    count = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by marker (---) or by lines if no marker
        if split_marker in content:
            entries = [e.strip() for e in content.split(split_marker) if e.strip()]
        else:
            entries = [line.strip() for line in content.splitlines() if line.strip()]

        for entry in entries:
            if len(entry) < 20:  # skip very short fragments
                continue
            add_memory(entry, metadata={
                "type": entry_type,
                "source_file": os.path.basename(file_path),
                "import_date": "2026-02-25"
            })
            count += 1
            if count % 10 == 0:
                print(f"  Imported {count} entries from {os.path.basename(file_path)}")

        print(f"Done: {count} entries imported from {file_path}")
        return count

    except Exception as e:
        print(f"Error importing {file_path}: {e}")
        return 0


if __name__ == "__main__":
    print("Starting batch import to ChromaDB...")

    # Active logs
    batch_import("C:/Kyrethys/backend/data/meditations.md", "meditation")
    batch_import("C:/Kyrethys/backend/data/dream_journal.txt", "dream")

    # Archives (adjust paths as needed)
    batch_import("C:/Kyrethys/backend/data/backup/dream_journal_archive_1_2026-02-25.txt", "dream")
    batch_import("C:/Kyrethys/backend/data/backup/meditations_archive_1.md", "meditation")

    print("\nImport completed.")