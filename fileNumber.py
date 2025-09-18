import os
import json
import shutil

def split_folder_preserve_json(folder_path, max_files=900):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    json_files = [f for f in files if f.lower().endswith((".json", ".geojson"))]
    image_files = [f for f in files if f.lower().endswith(".jpg") and f not in json_files]

    if len(image_files) <= max_files:
        return  # Skip folders with fewer images

    print(f"🔧 Splitting folder '{folder_path}' with {len(image_files)} images...")

    # Split images into chunks
    chunks = [image_files[i:i + max_files] for i in range(0, len(image_files), max_files)]
    base_folder = os.path.basename(folder_path)
    parent_folder = os.path.dirname(folder_path)

    # Load all features from JSONs
    all_features = []
    for json_file in json_files:
        json_path = os.path.join(folder_path, json_file)
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "features" in data:
                all_features.extend(data["features"])
        except Exception as e:
            print(f"⚠️ Failed to load JSON {json_file}: {e}")

    # Process each chunk
    for i, chunk in enumerate(chunks, start=1):
        new_folder_name = f"{base_folder}_{i}"
        new_folder_path = os.path.join(parent_folder, new_folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        # Move images
        for img in chunk:
            shutil.move(os.path.join(folder_path, img), os.path.join(new_folder_path, img))

        print(f"📁 Created: {new_folder_path} with {len(chunk)} images")

        # Filter features that reference images in this chunk
        updated_features = []
        for feature in all_features:
            props = feature.get("properties", {})
            for key in ["image", "image_path", "clipped"]:
                if key in props and props[key] in chunk:
                    updated_features.append(feature)
                    break

        if updated_features:
            new_json = {
                "type": "FeatureCollection",
                "features": updated_features
            }
            json_filename = f"{base_folder}_{i}.geojson"
            with open(os.path.join(new_folder_path, json_filename), "w", encoding="utf-8") as f:
                json.dump(new_json, f, indent=2, ensure_ascii=False)
            print(f"📝 JSON saved: {json_filename} in {new_folder_name}")

    # 🧹 Delete only JSON files from original folder
    for json_file in json_files:
        try:
            os.remove(os.path.join(folder_path, json_file))
            print(f"🗑️ Deleted JSON: {json_file}")
        except Exception as e:
            print(f"⚠️ Could not delete JSON {json_file}: {e}")

def process_all_folders(root_folder):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        split_folder_preserve_json(dirpath)

# 🔧 Run it on your root directory
process_all_folders(r"C:\Users\mhkwa\Desktop\pcl\webmapCopy")