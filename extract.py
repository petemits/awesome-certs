import json
import re

with open('README.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

data = []
current_category = None
current_sub = None

for line in lines:
    line = line.strip()
    
    if line.startswith('## '):
        current_category = line[3:].strip()
        current_sub = None
        data.append({'category': current_category, 'subcategory': None, 'courses': []})
    elif line.startswith('### '):
        current_sub = line[4:].strip()
        data.append({'category': current_category, 'subcategory': current_sub, 'courses': []})
    elif line.startswith('|') and current_category:
        parts = [p.strip() for p in line.split('|') if p.strip()]
        # Changed to >= 2 so it grabs Game Dev and other lists that have fewer columns
        if len(parts) >= 2 and 'Course Name' not in parts[0] and '---' not in parts[0]:
            name_text = parts[0]
            url = '#'
            match = re.search(r'\[(.*?)\]\((.*?)\)', name_text)
            if match:
                name = match.group(1)
                url = match.group(2)
            else:
                name = name_text
            
            course = {
                'name': name,
                'url': url,
                'provider': parts[1] if len(parts) > 1 else '',
                'level': parts[2] if len(parts) > 2 else '',
                'hours': parts[3] if len(parts) > 3 else ''
            }
            data[-1]['courses'].append(course)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
print('✅ Extracted full data!')
