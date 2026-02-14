#!/usr/bin/env python3
"""
🔥 TEMPLATE FIX V2 - IMPROVED FOR YOUR FILES
Handles ALL wrapper patterns including container-sm and tool-card-wrapper
"""

import os
import re
from pathlib import Path

# Colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header():
    print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
    print(f"{BLUE}{BOLD}🔥 TEMPLATE FIXER V2 - IMPROVED 🔥{RESET}")
    print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")

def fix_file_v2(filepath):
    """
    Enhanced version that handles multiple wrapper patterns:
    1. <div class="container tool-card-wrapper" ...>
    2. <div class="container-sm">
    3. <div style="max-width: 800px...">
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = False
        
        # Check if it's a tool page or blog page
        is_blog = '/blog/' in str(filepath)
        
        # Pattern 1: Remove <div class="container tool-card-wrapper" style="padding: 4rem 1.5rem;">
        if 'tool-card-wrapper' in content:
            pattern = r'<div\s+class="container\s+tool-card-wrapper"[^>]*>\s*'
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
            changes_made = True
        
        # Pattern 2: Remove <div class="container-sm">
        if '<div class="container-sm">' in content:
            content = content.replace('<div class="container-sm">', '')
            changes_made = True
        
        # Pattern 3: Remove nested white box wrapper
        # <div style="max-width: 800px; margin: 0 auto; background: white; padding: 3rem...">
        white_box_pattern = r'<div\s+style="[^"]*max-width:\s*800px[^"]*background:\s*white[^"]*">\s*'
        if re.search(white_box_pattern, content, re.IGNORECASE):
            content = re.sub(white_box_pattern, '', content, flags=re.IGNORECASE)
            changes_made = True
        
        # Pattern 4: Remove closing </div> tags before footer
        # We need to be careful here - count how many we removed
        if changes_made:
            # Find the footer and remove closing divs before it
            footer_pattern = r'(\s*</div>\s*){1,3}(<footer\s+class="footer")'
            
            # Count opening divs removed
            divs_removed = 0
            if 'tool-card-wrapper' in original_content:
                divs_removed += 1
            if '<div class="container-sm">' in original_content:
                divs_removed += 1
            if re.search(white_box_pattern, original_content, re.IGNORECASE):
                divs_removed += 1
            
            # Remove same number of closing divs
            if divs_removed > 0:
                # Replace with just the footer
                content = re.sub(
                    r'(</div>\s*){' + str(divs_removed) + r'}(<footer\s+class="footer")',
                    r'\2',
                    content,
                    flags=re.IGNORECASE
                )
        
        # Only write if changes were made
        if changes_made and content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Fixed successfully"
        else:
            return False, "No wrappers found or already clean"
    
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    print_header()
    
    repo_root = Path.cwd()
    print(f"{BOLD}Repository root: {repo_root}{RESET}\n")
    
    # All files to fix
    all_files = {
        'Blog Posts': [
            'blog/common-gst-mistakes.html',
            'blog/composition-scheme-guide.html',
            'blog/eway-bill-rules-2026.html',
            'blog/gst-penalty-calculator-guide.html',
            'blog/gst-rates-india-2026.html',
            'blog/gst-registration-process.html',
            'blog/gstr1-vs-gstr3b-differences.html',
            'blog/how-to-file-gst-return.html',
            'blog/hsn-code-complete-guide.html',
            'blog/input-tax-credit-guide.html',
            'blog/reverse-charge-mechanism-rcm.html',
            'blog/tds-under-gst-guide.html',
            'blog/what-is-gst-in-india.html',
        ],
        'Tool Pages': [
            'gst-calculator.html',
            'penalty-calculator.html',
            'gst-interest.html',
            'itc-calculator.html',
            'msme-payment-calculator.html',
            'gstr3b.html',
            'return-deadlines.html',
            'registration-checker.html',
            'budget-2026-changes.html',
            'gstin-verification.html',
            'hsn-finder.html',
            'invoice.html',
        ]
    }
    
    total_fixed = 0
    total_skipped = 0
    total_errors = 0
    
    for category, files in all_files.items():
        print(f"{BOLD}{BLUE}📝 FIXING {category.upper()} ({len(files)} files)...{RESET}\n")
        
        for file_path in files:
            filepath = repo_root / file_path
            
            if not filepath.exists():
                print(f"{RED}❌ Not found: {file_path}{RESET}")
                total_errors += 1
                continue
            
            success, message = fix_file_v2(filepath)
            
            if success:
                print(f"{GREEN}✅ Fixed: {file_path}{RESET}")
                total_fixed += 1
            else:
                if "No wrappers" in message or "already clean" in message.lower():
                    print(f"{YELLOW}⏭️  Skipped: {file_path} ({message}){RESET}")
                    total_skipped += 1
                else:
                    print(f"{RED}❌ Failed: {file_path} - {message}{RESET}")
                    total_errors += 1
        
        print()
    
    # Summary
    total = total_fixed + total_skipped + total_errors
    print(f"{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}📊 SUMMARY{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")
    print(f"Total files processed: {BOLD}{total}{RESET}")
    print(f"{GREEN}✅ Fixed: {BOLD}{total_fixed}{RESET}")
    print(f"{YELLOW}⏭️  Skipped: {BOLD}{total_skipped}{RESET}")
    print(f"{RED}❌ Errors: {BOLD}{total_errors}{RESET}\n")
    
    if total_fixed > 0:
        print(f"{GREEN}{BOLD}🔥 SUCCESS! {total_fixed} files updated! 🔥{RESET}\n")
        print(f"{YELLOW}Next steps:{RESET}")
        print(f"1. Test a few pages in browser")
        print(f"2. In PowerShell: git add .")
        print(f"3. Then: git commit -m \"Fix templates v2\"")
        print(f"4. Then: git push\n")
    else:
        print(f"{YELLOW}ℹ️  No changes needed - files may already be clean{RESET}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}⚠️  Interrupted by user{RESET}\n")
    except Exception as e:
        print(f"\n{RED}❌ Fatal error: {str(e)}{RESET}\n")
        raise
