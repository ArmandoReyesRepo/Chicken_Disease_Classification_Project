import pathlib

root = pathlib.Path("/Users/armandoreyesmartinez/00_End_to_End_ML/Chicken_Disease_Classification_Project")
for path in root.rglob("*.py"):
    text = path.read_text()
    if "assertRaisesRegexp" in text:
        new_text = text.replace("assertRaisesRegexp", "assertRaisesRegexpp")
        path.write_text(new_text)
        print(f"🔄 Reverted: {path}")