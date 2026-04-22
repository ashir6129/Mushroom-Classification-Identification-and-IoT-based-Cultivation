
import os

DATASET_DIR = "/home/ashirkhan/Updated Data set/raw_images_renamed"
DELETE_LIST_FILE = "/home/ashirkhan/Updated Data set/to_delete.txt"

def main():
    if not os.path.exists(DELETE_LIST_FILE):
        print(f"File not found: {DELETE_LIST_FILE}")
        print("Please create this file and paste the list of images to delete (one per line).")
        print("Expected format: category_name/image_name.jpg")
        return

    with open(DELETE_LIST_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines:
        print("The deletion list is empty.")
        return

    print(f"Starting deletion of {len(lines)} images...")
    
    deleted_count = 0
    not_found_count = 0
    
    for relative_path in lines:
        full_path = os.path.join(DATASET_DIR, relative_path)
        
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                print(f"✅ Deleted: {relative_path}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Error deleting {relative_path}: {e}")
        else:
            print(f"⚠️  Not found: {relative_path}")
            not_found_count += 1

    print("\n--- Summary ---")
    print(f"Successfully deleted: {deleted_count}")
    print(f"Files not found: {not_found_count}")
    print("----------------")

if __name__ == "__main__":
    main()
