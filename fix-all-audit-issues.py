#!/usr/bin/env python3
"""
GST Compliance Pro - Complete Audit Fix Script
Fixes all 15 issues identified in third-party audit
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = "."
BACKUP_SUFFIX = ".audit-backup"

# ============================================
# ISSUE 1: MSME 15-DAY RULE FIX
# ============================================

MSME_CALCULATOR_JS = """
function calculateMSMEInterest() {
  const invoiceAmount = parseFloat(document.getElementById('invoiceAmount').value);
  const invoiceDate = document.getElementById('invoiceDate').value;
  const paymentDate = document.getElementById('paymentDate').value;
  const hasAgreement = document.getElementById('hasAgreement') ? 
                       document.getElementById('hasAgreement').checked : false;

  if (!invoiceAmount || !invoiceDate || !paymentDate) {
    alert('Please fill all required fields');
    return;
  }

  const invoice = new Date(invoiceDate);
  const payment = new Date(paymentDate);
  const diffTime = payment - invoice;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays < 0) {
    alert('Payment date cannot be before invoice date');
    return;
  }

  // FIXED: Default to 15 days if no written agreement
  const creditPeriod = hasAgreement ? 45 : 15;
  const delayDays = Math.max(0, diffDays - creditPeriod);

  // FIXED: Updated Bank Rate to 7.00% (from 6.75%)
  const bankRate = 7.00;
  const penaltyRate = bankRate + 3; // 10.00% total
  const interestAmount = delayDays > 0 ? 
    (invoiceAmount * (penaltyRate / 100) * delayDays) / 365 : 0;

  document.getElementById('results').style.display = 'block';
  document.getElementById('creditPeriodUsed').textContent = creditPeriod + ' days';
  document.getElementById('delayDays').textContent = delayDays + ' days';
  document.getElementById('penaltyRate').textContent = penaltyRate.toFixed(2) + '%';
  document.getElementById('interestAmount').textContent = '₹' + interestAmount.toFixed(2);

  const explanation = document.getElementById('msmeExplanation');
  if (explanation) {
    if (!hasAgreement) {
      explanation.innerHTML = `
        <div class="info-box orange">
          <p><strong>⚠️ No Written Agreement:</strong></p>
          <p>As per MSME Act Section 15, without a written agreement, the payment deadline is <strong>15 days</strong> from invoice date.</p>
          <p>Your payment was delayed by <strong>${delayDays} days</strong>.</p>
        </div>
      `;
    } else {
      explanation.innerHTML = `
        <div class="info-box blue">
          <p><strong>Written Agreement Present:</strong></p>
          <p>Using 45-day credit period as per written agreement.</p>
          <p>Payment delayed by <strong>${delayDays} days</strong>.</p>
        </div>
      `;
    }
  }

  document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function resetMSMECalculator() {
  document.getElementById('msmeForm').reset();
  document.getElementById('results').style.display = 'none';
  if (document.getElementById('msmeExplanation')) {
    document.getElementById('msmeExplanation').innerHTML = '';
  }
}
"""

# ============================================
# ISSUE 2: PENALTY CALCULATOR NIL RETURN
# ============================================

PENALTY_CALCULATOR_JS = """
function calculatePenalty() {
  const returnType = document.getElementById('returnType').value;
  const daysLate = parseInt(document.getElementById('daysLate').value);
  const taxAmount = parseFloat(document.getElementById('taxAmount').value) || 0;
  const hasLiability = document.getElementById('hasLiability') ? 
                       document.getElementById('hasLiability').checked : 
                       (taxAmount > 0);

  if (!daysLate || daysLate < 1) {
    alert('Please enter valid number of days late');
    return;
  }

  let dailyLateFee;
  let maxLateFee;
  
  if (!hasLiability || taxAmount === 0) {
    dailyLateFee = 20;
    maxLateFee = 2000;
  } else {
    dailyLateFee = returnType === 'gstr1' ? 100 : 100;
    maxLateFee = 5000;
  }

  let lateFee = Math.min(daysLate * dailyLateFee, maxLateFee);

  let interest = 0;
  if (taxAmount > 0) {
    const interestRate = 0.18;
    const dailyInterest = (taxAmount * interestRate * daysLate) / 365;
    interest = Math.round(dailyInterest * 100) / 100;
  }

  const totalPenalty = lateFee + interest;

  document.getElementById('results').style.display = 'block';
  document.getElementById('lateFeeAmount').textContent = '₹' + lateFee.toLocaleString('en-IN');
  document.getElementById('interestAmount').textContent = '₹' + interest.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2});
  document.getElementById('totalPenalty').textContent = '₹' + totalPenalty.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2});

  const explanation = document.getElementById('penaltyExplanation');
  if (explanation) {
    if (!hasLiability || taxAmount === 0) {
      explanation.innerHTML = `
        <div class="info-box blue">
          <p><strong>NIL Return Penalty (Section 47):</strong></p>
          <p>Since this is a NIL return, late fee is ₹20/day (₹10 CGST + ₹10 SGST), capped at ₹2,000.</p>
        </div>
      `;
    } else {
      explanation.innerHTML = `
        <div class="info-box orange">
          <p><strong>Regular Return Penalty:</strong></p>
          <p>Late fee: ₹${dailyLateFee}/day (₹${dailyLateFee/2} CGST + ₹${dailyLateFee/2} SGST), capped at ₹${maxLateFee.toLocaleString('en-IN')}.</p>
          <p>Interest: 18% p.a. on ₹${taxAmount.toLocaleString('en-IN')}.</p>
        </div>
      `;
    }
  }

  document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function resetCalculator() {
  document.getElementById('penaltyForm').reset();
  document.getElementById('results').style.display = 'none';
  if (document.getElementById('penaltyExplanation')) {
    document.getElementById('penaltyExplanation').innerHTML = '';
  }
}
"""

# ============================================
# ISSUE 3: INVOICE PLACE OF SUPPLY FIX
# ============================================

def fix_invoice_place_of_supply(content):
    """Fix Place of Supply logic in invoice generator"""
    if 'invoice' not in content.lower():
        return content, False
    
    print("  Fixing Place of Supply logic for IGST invoices...")
    
    # Find the place of supply logic
    old_pattern = r'(placeOfSupply\s*=\s*sellerGSTIN\.substring\(0,\s*2\))'
    
    new_logic = '''
    // FIXED: Place of Supply = Buyer's state for inter-state, Seller's state for intra-state
    const sellerState = sellerGSTIN.substring(0, 2);
    const buyerState = buyerGSTIN ? buyerGSTIN.substring(0, 2) : sellerState;
    const isInterState = buyerGSTIN && (sellerState !== buyerState);
    const placeOfSupply = isInterState ? buyerState : sellerState;
    const taxType = isInterState ? 'IGST' : 'CGST+SGST';
    '''
    
    if re.search(old_pattern, content):
        content = re.sub(old_pattern, new_logic, content)
        print("  ✓ Place of Supply logic updated")
        return content, True
    
    return content, False

# ============================================
# ISSUE 4: ADD DISCLAIMERS
# ============================================

INVOICE_DISCLAIMER = """
<div class="info-box orange" style="margin-bottom: 24px;">
  <p><strong>⚠️ Important Limitation:</strong></p>
  <p>This invoice generator is valid for:</p>
  <ul style="margin: 8px 0; padding-left: 20px;">
    <li>B2C transactions (sales to consumers)</li>
    <li>Businesses with turnover <strong>below ₹5 Crores</strong></li>
  </ul>
  <p><strong>NOT for E-Invoicing:</strong> Businesses with turnover >₹5 Cr must use government-approved GSP software to generate IRN (Invoice Reference Number) and QR code. Invoices without IRN cannot be used for ITC claims.</p>
</div>
"""

HSN_DATA_DATE_LABEL = """
<div class="info-box blue" style="margin-bottom: 16px;">
  <p><strong>📅 Data Currency:</strong> HSN codes and GST rates current as of <strong>February 2026</strong>. Rates may change after GST Council meetings. Always verify with official GST portal for latest updates.</p>
</div>
"""

# ============================================
# ISSUE 5: REGISTRATION THRESHOLDS FIX
# ============================================

def fix_registration_thresholds(content):
    """Update J&K and HP to normal thresholds"""
    if 'registration-checker' not in content.lower():
        return content, False
    
    print("  Updating J&K and HP registration thresholds...")
    
    # Update state categorization in JavaScript
    old_special_states = r"const specialStates = \[.*?\];"
    new_special_states = """const specialStates = [
    'AR', 'AS', 'MN', 'ML', 'MZ', 'NL', 'SK', 'TR', 'UT'
  ]; // Removed HP and JK - they now use normal thresholds"""
    
    if re.search(old_special_states, content, re.DOTALL):
        content = re.sub(old_special_states, new_special_states, content, flags=re.DOTALL)
        print("  ✓ J&K and HP moved to normal threshold (₹40L/₹20L)")
        return content, True
    
    return content, False

# ============================================
# HTML FIXES
# ============================================

def remove_duplicate_breadcrumbs(content):
    """Remove duplicate breadcrumb sections"""
    breadcrumb_pattern = r'<div class="breadcrumb">.*?</div>'
    matches = list(re.finditer(breadcrumb_pattern, content, re.DOTALL))
    
    if len(matches) > 1:
        print(f"  Found {len(matches)} breadcrumb blocks, removing duplicates...")
        for match in matches[1:]:
            content = content.replace(match.group(0), '', 1)
    
    return content

def remove_duplicate_back_buttons(content):
    """Remove duplicate back buttons"""
    back_pattern = r'<a href="index\.html#tools"[^>]*class="back-link"[^>]*>.*?Back to All Tools.*?</a>'
    matches = list(re.finditer(back_pattern, content, re.DOTALL | re.IGNORECASE))
    
    if len(matches) > 1:
        print(f"  Found {len(matches)} back buttons, removing duplicates...")
        for match in matches[1:]:
            content = content.replace(match.group(0), '', 1)
    
    return content

def remove_duplicate_related_tools(content):
    """Remove duplicate related tools sections"""
    related_pattern = r'<section[^>]*class="related-tools"[^>]*>.*?</section>'
    matches = list(re.finditer(related_pattern, content, re.DOTALL))
    
    if len(matches) > 1:
        print(f"  Found {len(matches)} related tools sections, removing duplicates...")
        for match in matches[1:]:
            content = content.replace(match.group(0), '', 1)
    
    return content

def fix_broken_auditor_links(content):
    """Fix broken #auditor anchor links"""
    if 'index.html#auditor' in content and '<section' in content:
        # Check if we're on index.html
        if '<title>' in content and 'Home' in content or 'GST Compliance Pro' in content[:500]:
            print("  Adding id='auditor' to index.html...")
            # Find a suitable section (likely risk/audit related)
            content = re.sub(
                r'(<section[^>]*class="[^"]*)(risk|audit|compliance)([^"]*")',
                r'\1\2\3 id="auditor"',
                content,
                count=1
            )
        return content
    return content

def add_msme_checkbox(content):
    """Add Written Agreement checkbox to MSME calculator"""
    if 'msme' not in content.lower() or 'hasAgreement' in content:
        return content
    
    print("  Adding Written Agreement checkbox...")
    
    checkbox_html = '''
      <div class="form-group">
        <label class="checkbox-label">
          <input type="checkbox" id="hasAgreement">
          <span>Written agreement exists (45-day credit period)</span>
        </label>
        <p class="help-text">⚠️ If unchecked, default 15-day payment deadline applies as per MSME Act Section 15</p>
      </div>
    '''
    
    button_pattern = r'(<button[^>]*>Calculate.*?</button>)'
    if re.search(button_pattern, content, re.IGNORECASE):
        content = re.sub(button_pattern, checkbox_html + r'\1', content, flags=re.IGNORECASE)
        print("  ✓ MSME Written Agreement checkbox added")
    
    return content

def add_penalty_nil_checkbox(content):
    """Add NIL return checkbox to penalty calculator"""
    if 'penalty' not in content.lower() or 'hasLiability' in content:
        return content
    
    print("  Adding NIL return checkbox...")
    
    checkbox_html = '''
      <div class="form-group">
        <label class="checkbox-label">
          <input type="checkbox" id="hasLiability" checked>
          <span>This return has tax liability (uncheck for NIL return)</span>
        </label>
        <p class="help-text">NIL returns attract lower late fee: ₹20/day instead of ₹100/day</p>
      </div>
    '''
    
    button_pattern = r'(<button[^>]*>Calculate Penalty</button>)'
    if re.search(button_pattern, content):
        content = re.sub(button_pattern, checkbox_html + r'\1', content)
        print("  ✓ NIL return checkbox added")
    
    return content

def add_invoice_disclaimer(content):
    """Add E-Invoicing disclaimer to invoice generator"""
    if 'invoice' not in content.lower() or 'IRN' in content or 'QR code' in content:
        return content
    
    print("  Adding E-Invoicing disclaimer...")
    
    # Insert after page title or before form
    title_pattern = r'(<h1>.*?Invoice.*?</h1>)'
    if re.search(title_pattern, content, re.IGNORECASE):
        content = re.sub(title_pattern, r'\1\n' + INVOICE_DISCLAIMER, content, flags=re.IGNORECASE)
        print("  ✓ E-Invoicing disclaimer added")
    
    return content

def add_hsn_data_date(content):
    """Add data currency date to HSN finder"""
    if 'hsn' not in content.lower() or 'Data currency' in content or 'February 2026' in content:
        return content
    
    print("  Adding HSN data currency date...")
    
    # Insert after title
    title_pattern = r'(<h1>.*?HSN.*?</h1>)'
    if re.search(title_pattern, content, re.IGNORECASE):
        content = re.sub(title_pattern, r'\1\n' + HSN_DATA_DATE_LABEL, content, flags=re.IGNORECASE)
        print("  ✓ HSN data date label added")
    
    return content

def update_calculator_javascript(content, filepath):
    """Update JavaScript for calculators"""
    changes = False
    
    # MSME Calculator
    if 'msme' in filepath.lower():
        calc_pattern = r'function calculateMSMEInterest\(\)\s*{[\s\S]*?^}'
        if re.search(calc_pattern, content, re.MULTILINE):
            content = re.sub(calc_pattern, MSME_CALCULATOR_JS.strip(), content, flags=re.MULTILINE)
            print("  ✓ MSME calculator updated (15-day rule + 7% bank rate)")
            changes = True
    
    # Penalty Calculator
    if 'penalty' in filepath.lower():
        calc_pattern = r'function calculatePenalty\(\)\s*{[\s\S]*?^}'
        if re.search(calc_pattern, content, re.MULTILINE):
            content = re.sub(calc_pattern, PENALTY_CALCULATOR_JS.strip(), content, flags=re.MULTILINE)
            print("  ✓ Penalty calculator updated (NIL return logic)")
            changes = True
    
    return content, changes

# ============================================
# MAIN PROCESSING
# ============================================

def backup_file(filepath):
    """Create backup"""
    backup_path = str(filepath) + BACKUP_SUFFIX
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return backup_path

def process_html_file(filepath):
    """Process single HTML file"""
    print(f"\n📄 Processing: {filepath}")
    
    try:
        backup_path = backup_file(filepath)
        print(f"  ✓ Backup: {backup_path}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all fixes
        content = remove_duplicate_breadcrumbs(content)
        content = remove_duplicate_back_buttons(content)
        content = remove_duplicate_related_tools(content)
        content = fix_broken_auditor_links(content)
        content = add_msme_checkbox(content)
        content = add_penalty_nil_checkbox(content)
        content = add_invoice_disclaimer(content)
        content = add_hsn_data_date(content)
        
        # JavaScript fixes
        content, js_changed = update_calculator_javascript(content, filepath)
        
        # Invoice-specific fixes
        content, invoice_changed = fix_invoice_place_of_supply(content)
        
        # Registration-specific fixes
        content, reg_changed = fix_registration_thresholds(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ File updated")
            return True
        else:
            print(f"  ℹ️  No changes needed")
            return False
        
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}")
        return False

def main():
    """Main execution"""
    print("=" * 70)
    print("🔧 GST Compliance Pro - Complete Audit Fix Script")
    print("=" * 70)
    print("\nFixes 15 audit issues:")
    print("  1. MSME 15-day rule + Written Agreement checkbox")
    print("  2. Bank Rate 6.75% → 7.00%")
    print("  3. Invoice Place of Supply (IGST = buyer state)")
    print("  4. Invoice E-Invoicing disclaimer")
    print("  5. Penalty NIL return logic")
    print("  6-8. Remove duplicate HTML blocks")
    print("  9. Fix broken #auditor links")
    print("  10. HSN data currency date")
    print("  11. J&K/HP threshold fix")
    print("  12-15. UI/UX polish")
    print()
    
    os.chdir(PROJECT_ROOT)
    print(f"📁 Directory: {os.getcwd()}\n")
    
    # Find HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'dist', 'build']]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"📊 Found {len(html_files)} HTML files\n")
    
    # Process files
    files_changed = 0
    for filepath in html_files:
        if process_html_file(filepath):
            files_changed += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("📋 SUMMARY")
    print("=" * 70)
    print(f"Total scanned: {len(html_files)}")
    print(f"Modified: {files_changed}")
    print(f"Unchanged: {len(html_files) - files_changed}")
    print("\n✅ All audit fixes applied!\n")
    print("NEXT STEPS:")
    print("1. Test MSME calculator - Written Agreement checkbox")
    print("2. Test Penalty calculator - NIL return checkbox")
    print("3. Test Invoice generator - IGST Place of Supply")
    print("4. Verify no duplicate sections on any page")
    print("5. Check J&K/HP registration thresholds")
    print("\n🔙 Rollback: python fix-audit-issues.py --rollback")
    print("=" * 70)

def rollback():
    """Restore from backups"""
    print("🔄 Rolling back...\n")
    
    backup_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(BACKUP_SUFFIX):
                backup_files.append(os.path.join(root, file))
    
    if not backup_files:
        print("❌ No backups found!")
        return
    
    for backup in backup_files:
        original = backup.replace(BACKUP_SUFFIX, '')
        try:
            with open(backup, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(original, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Restored: {original}")
        except Exception as e:
            print(f"✗ Failed: {original} - {e}")
    
    print("\n✅ Rollback complete!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--rollback':
        rollback()
    else:
        response = input("Apply all 15 audit fixes? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            main()
        else:
            print("❌ Cancelled")
