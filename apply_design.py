import os
import re

def update_html_file(filepath, is_sub):
    prefix = "../" if is_sub else ""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # If it's already wrapped or is the homepage, skip the wrapping logic
    if 'class="tool-card-wrapper"' in content or "index.html" in filepath:
        return

    # 1. Identify the content between the Disclaimer and Footer (or body tags)
    # We will wrap everything currently inside <body> into a professional container
    body_pattern = r'(<body[^>]*>)(.*?)(<footer|</body>)'
    
    wrapper_html = f'''\\1
    <div class="container tool-card-wrapper" style="padding: 4rem 1.5rem;">
        <div style="max-width: 800px; margin: 0 auto; background: white; padding: 3rem; border-radius: var(--radius-2xl); border: 2px solid var(--gray-200); box-shadow: var(--shadow-lg);">
            \\2
        </div>
    </div>
    \\3'''

    new_content = re.sub(body_pattern, wrapper_html, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"✨ Card Wrap Applied: {filepath}")

# Run for all files
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html') and "index.html" not in file:
            update_html_file(os.path.join(root, file), root != ".")