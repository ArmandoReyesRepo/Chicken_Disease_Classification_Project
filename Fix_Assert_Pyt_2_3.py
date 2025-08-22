## https://chatgpt.com/share/68a7a3ac-c77c-800a-b0d8-1dded1a4c405


import pathlib

root = pathlib.Path("/Users/armandoreyesmartinez/00_End_to_End_ML/Chicken_Disease_Classification_Project")  # change to your project root
for path in root.rglob("*.py"):
    text = path.read_text()
    if "assertRaisesRegexp" in text:
        new_text = text.replace("assertRaisesRegexp", "assertRaisesRegexp")
        path.write_text(new_text)
        print(f"✅ Fixed: {path}")

