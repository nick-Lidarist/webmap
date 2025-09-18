import os
import json

def rename_images_and_update_json(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        # Get folder prefix from relative path
        rel_path = os.path.relpath(dirpath, root_folder)
        folder_prefix = rel_path.replace(os.sep, "_") if rel_path != "." else ""

        # Rename .jpg files
        for filename in filenames:
            if filename.lower().endswith(".jpg"):
                old_path = os.path.join(dirpath, filename)
                new_filename = f"{folder_prefix}_{filename}" if folder_prefix else filename
                new_path = os.path.join(dirpath, new_filename)

                if filename != new_filename:
                    os.rename(old_path, new_path)
                    print(f"✅ Renamed: {filename} → {new_filename}")

        # Update .json and .geojson files
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
                            for key in ["image", "image_path"]:
                                if key in props and isinstance(props[key], str):
                                    old_img = props[key]
                                    new_img = f"{folder_prefix}_{old_img}" if folder_prefix else old_img
                                    if old_img != new_img:
                                        props[key] = new_img
                                        changed = True

                    if changed:
                        with open(json_path, "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        print(f"📝 Updated JSON: {filename}")

                except Exception as e:
                    print(f"⚠️ Failed to process {filename}: {e}")

# 🔧 Run it on your folder
rename_images_and_update_json(r"C:\Users\mhkwa\Desktop\pcl\webmapCopy")