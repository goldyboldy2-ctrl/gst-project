#!/usr/bin/env python3
"""
🔥 TEMPLATE FIX AUTOMATION - GST Compliance Pro
Removes ugly white wrapper boxes from all blog and tool pages
Makes everything look fire like the homepage!
"""

import os
import re
from pathlib import Path

# ANSI colors for output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header():
    """Print fancy header"""
    print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
    print(f"{BLUE}{BOLD}🔥 GST COMPLIANCE PRO - TEMPLATE FIXER 🔥{RESET}")
    print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")

def remove_ugly_wrappers(content):
    """
    Remove the ugly white wrapper divs from HTML content
    
    Removes:
    <div class="container tool-card-wrapper" style="padding: 4rem 1.5rem;">
        <div style="max-width: 800px; margin: 0 auto; background: white; padding: 3rem...">
    
    And their closing </div></div> tags
    """
    
    # Pattern 1: Opening wrapper (container tool-card-wrapper)
    pattern1 = r'<div\s+class="container\s+tool-card-wrapper"[^>]*>\s*'
    
    # Pattern 2: Inner white box wrapper
    pattern2 = r'<div\s+style="max-width:\s*800px;[^"]*background:\s*white[^"]*">\s*'
    
    # Remove opening wrappers
    content = re.sub(pattern1, '', content, flags=re.IGNORECASE)
    content = re.sub(pattern2, '', content, flags=re.IGNORECASE)
    
    # Now we need to remove the corresponding closing </div></div> tags
    # We'll look for </div></div> patterns near the footer
    
    # Pattern: </div> </div> before footer (with optional whitespace)
    # We'll be conservative and only remove the last occurrence before </body>
    footer_pattern = r'(\s*</div>\s*</div>\s*)(<footer\s+class="footer")'
    content = re.sub(footer_pattern, r'\2', content, flags=re.IGNORECASE)
    
    return content

def fix_blog_file(filepath):
    """Fix a single blog file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has the ugly wrapper
        if 'tool-card-wrapper' not in content:
            return False, "Already clean"
        
        # Remove wrappers
        new_content = remove_ugly_wrappers(content)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Fixed successfully"
    
    except Exception as e:
        return False, f"Error: {str(e)}"

def fix_tool_file(filepath):
    """Fix a single tool file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has the ugly wrapper
        if 'tool-card-wrapper' not in content:
            return False, "Already clean"
        
        # Remove wrappers
        new_content = remove_ugly_wrappers(content)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Fixed successfully"
    
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Main execution"""
    print_header()
    
    # Get repository root (assuming script is in outputs folder)
    # User should run this from the repo root
    repo_root = Path.cwd()
    
    print(f"{BOLD}Repository root: {repo_root}{RESET}\n")
    
    # Blog files to fix
    blog_files = [
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
    ]
    
    # Tool files to fix
    tool_files = [
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
    
    # Statistics
    total_files = len(blog_files) + len(tool_files)
    fixed_count = 0
    skipped_count = 0
    error_count = 0
    
    # Fix blog files
    print(f"{BOLD}{BLUE}📝 FIXING BLOG FILES ({len(blog_files)} files)...{RESET}\n")
    for blog_file in blog_files:
        filepath = repo_root / blog_file
        
        if not filepath.exists():
            print(f"{RED}❌ Not found: {blog_file}{RESET}")
            error_count += 1
            continue
        
        success, message = fix_blog_file(filepath)
        
        if success:
            print(f"{GREEN}✅ Fixed: {blog_file}{RESET}")
            fixed_count += 1
        else:
            if "Already clean" in message:
                print(f"{YELLOW}⏭️  Skipped: {blog_file} ({message}){RESET}")
                skipped_count += 1
            else:
                print(f"{RED}❌ Failed: {blog_file} - {message}{RESET}")
                error_count += 1
    
    print()
    
    # Fix tool files
    print(f"{BOLD}{BLUE}🔧 FIXING TOOL FILES ({len(tool_files)} files)...{RESET}\n")
    for tool_file in tool_files:
        filepath = repo_root / tool_file
        
        if not filepath.exists():
            print(f"{RED}❌ Not found: {tool_file}{RESET}")
            error_count += 1
            continue
        
        success, message = fix_tool_file(filepath)
        
        if success:
            print(f"{GREEN}✅ Fixed: {tool_file}{RESET}")
            fixed_count += 1
        else:
            if "Already clean" in message:
                print(f"{YELLOW}⏭️  Skipped: {tool_file} ({message}){RESET}")
                skipped_count += 1
            else:
                print(f"{RED}❌ Failed: {tool_file} - {message}{RESET}")
                error_count += 1
    
    # Print summary
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}📊 SUMMARY{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")
    
    print(f"Total files processed: {BOLD}{total_files}{RESET}")
    print(f"{GREEN}✅ Fixed: {BOLD}{fixed_count}{RESET}")
    print(f"{YELLOW}⏭️  Skipped: {BOLD}{skipped_count}{RESET}")
    print(f"{RED}❌ Errors: {BOLD}{error_count}{RESET}")
    
    if fixed_count > 0:
        print(f"\n{GREEN}{BOLD}🔥 SUCCESS! Your site now looks FIRE! 🔥{RESET}")
        print(f"\n{YELLOW}Next steps:{RESET}")
        print(f"1. Test a few pages to verify changes")
        print(f"2. Commit to Git: git add . && git commit -m 'Remove ugly wrappers'")
        print(f"3. Push to GitHub")
    else:
        print(f"\n{YELLOW}ℹ️  All files are already clean or no changes needed.{RESET}")
    
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}⚠️  Interrupted by user{RESET}\n")
    except Exception as e:
        print(f"\n{RED}❌ Fatal error: {str(e)}{RESET}\n")
        raise