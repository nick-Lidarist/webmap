import os
import json
import re

def clean_filename(filename, folder_prefix):
    # Remove any existing folder-like prefix from filename
    pattern = re.compile(rf"^{folder_prefix}_.+?_(.+\.jpg)$")
    match = pattern.match(filename)
    if match:
        return match.group(1)  # Extract original filename
    return filename

def rename_images_and_update_json(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        rel_path = os.path.relpath(dirpath, root_folder)
        folder_prefix = rel_path.replace(os.sep, "_") if rel_path != "." else ""

        rename_map = {}

        # 🔁 Rename .jpg files
        for filename in filenames:
            if filename.lower().endswith(".jpg"):
                old_path = os.path.join(dirpath, filename)

                # Normalize filename by removing any existing prefix
                base_name = clean_filename(filename, folder_prefix)
                new_filename = f"{folder_prefix}_{base_name}" if folder_prefix else base_name
                new_path = os.path.join(dirpath, new_filename)

                if filename != new_filename:
                    os.rename(old_path, new_path)
                    rename_map[filename] = new_filename
                    rename_map[base_name] = new_filename  # Handle both original and previously renamed
                    print(f"✅ Renamed: {filename} → {new_filename}")

        # 📝 Update JSON references
        for filename in filenames:
            if filename.lower().endswith((".json", ".geojson")):
                json_path = os.path.join(dirpath, filename)
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    changed = False
                    if isinstance(data, dict) and "features" in data:
                        for feature in data["features"]:
                            props = feature.get("properties", {})
                            for key in ["image", "image_path", "clipped"]:
                                if key in props and isinstance(props[key], str):
                                    original = props[key]
                                    normalized = clean_filename(original, folder_prefix)
                                    new_img = f"{folder_prefix}_{normalized}" if folder_prefix else normalized
                                    if original != new_img:
                                        props[key] = new_img
                                        changed = True

                    if changed:
                        with open(json_path, "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        print(f"📝 Updated JSON: {filename}")

                except Exception as e:
                    print(f"⚠️ Failed to process {filename}: {e}")

# 🔧 Run it
rename_images_and_update_json(r"C:\Users\mhkwa\Desktop\pcl\webmapCopy")