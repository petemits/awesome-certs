import json

# Read the data
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Read the current HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the external script tag with the inline data
inline_data = f"<script>const courseData = {json.dumps(data)};</script>"
html = html.replace('<script src="data.js"></script>', inline_data)

# Save the final, bulletproof index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Injected data directly into index.html!")
