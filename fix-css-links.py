#!/usr/bin/env python3
"""
🔥 CSS LINK FIXER - Replace old style.css with master-style.css
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
    print(f"{BLUE}{BOLD}🔥 CSS LINK FIXER 🔥{RESET}")
    print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")

def fix_css_link(filepath):
    """Replace style.css with master-style.css"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: <link rel="stylesheet" href="style.css" />
        pattern1 = r'<link\s+rel="stylesheet"\s+href="style\.css"\s*/>'
        replacement1 = '<link rel="stylesheet" href="master-style.css">'
        content = re.sub(pattern1, replacement1, content, flags=re.IGNORECASE)
        
        # Pattern 2: <link href="style.css" rel="stylesheet" />
        pattern2 = r'<link\s+href="style\.css"\s+rel="stylesheet"\s*/>'
        replacement2 = '<link rel="stylesheet" href="master-style.css">'
        content = re.sub(pattern2, replacement2, content, flags=re.IGNORECASE)
        
        # Pattern 3: For blog files, need to go up one directory
        if '/blog/' in str(filepath):
            # Replace href="master-style.css" with href="../master-style.css"
            content = content.replace('href="master-style.css"', 'href="../master-style.css"')
        
        # Check if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Updated style.css → master-style.css"
        else:
            return False, "No style.css found or already using master-style.css"
    
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    print_header()
    
    repo_root = Path.cwd()
    print(f"{BOLD}Repository root: {repo_root}{RESET}\n")
    
    # All files to fix
    all_files = {
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
        ],
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
        'Blog Index': [
            'blog/index.html',
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
            
            success, message = fix_css_link(filepath)
            
            if success:
                print(f"{GREEN}✅ Fixed: {file_path}{RESET}")
                total_fixed += 1
            else:
                print(f"{YELLOW}⏭️  Skipped: {file_path} ({message}){RESET}")
                total_skipped += 1
        
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
        print(f"{GREEN}{BOLD}🔥 SUCCESS! All CSS links updated! 🔥{RESET}\n")
        print(f"{YELLOW}Next steps:{RESET}")
        print(f"1. In PowerShell: git add .")
        print(f"2. Then: git commit -m \"Fix CSS links to master-style.css\"")
        print(f"3. Then: git push")
        print(f"4. Wait 2-3 minutes, then refresh your site!\n")
    else:
        print(f"{YELLOW}ℹ️  All files already using master-style.css!{RESET}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}⚠️  Interrupted by user{RESET}\n")
    except Exception as e:
        print(f"\n{RED}❌ Fatal error: {str(e)}{RESET}\n")
        raise
