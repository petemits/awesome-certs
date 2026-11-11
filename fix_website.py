import re

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Aggressive CSS (using !important to force animations to work)
css_code = """
<style>
    @keyframes slideUpFade {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    p, table, ul { animation: slideUpFade 1.2s ease-out forwards; }
    .video-wrapper { width: 100%; max-width: 800px; margin: 20px auto; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 16px rgba(0,0,0,0.3); }
    .video-wrapper video { width: 100%; display: block; }
</style>
"""

# 2. The Video HTML
video_code = """
<div class="video-wrapper">
    <video autoplay loop muted playsinline>
        <source src="https://assets.mixkit.co/videos/preview/mixkit-stars-in-space-1610-large.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>
"""

# 3. Inject CSS before </head>
if '</head>' in html:
    html = html.replace('</head>', css_code + '</head>')
else:
    html = css_code + html

# 4. Inject Video right after the opening body tag, regardless of class/id
# This regex finds <body> or <body class="..."> and replaces it
html = re.sub(r'(<body[^>]*>)', r'\1' + video_code, html, count=1)

# 5. Save the file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Code forcefully injected!")
