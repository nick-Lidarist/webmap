import os
import json

# ✅ Your GitHub Pages base URL
base_url = "https://nick-Lidarist.github.io/webmap"

# ✅ Local folder to scan (your repo root)
local_root = r"C:\Users\mhkwa\Desktop\pcl\webmapCopy"

# ✅ File types to include
valid_exts = {".jpg", ".json", ".geojson"}

# ✅ Output structure
manifest = {
    "jpg": [],
    "json": [],
    "geojson": []
}

# 🔍 Recursively scan all folders
for foldername, subfolders, filenames in os.walk(local_root):
    for filename in filenames:
        ext = os.path.splitext(filename)[1].lower()
        if ext in valid_exts:
            local_path = os.path.join(foldername, filename)

            # Get relative path from repo root
            rel_path = os.path.relpath(local_path, local_root).replace("\\", "/")

            # Build full GitHub Pages URL
            full_url = f"{base_url}/{rel_path}"

            # Add to manifest
            manifest[ext.lstrip(".")].append(full_url)

# 💾 Save manifest.json in the root folder
output_path = os.path.join(local_root, "manifest.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

# ✅ Summary
print(f"✅ manifest.json created with:")
for key in manifest:
    print(f"  {key}: {len(manifest[key])} files")