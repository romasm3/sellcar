"""
Auto-fix script for views.py indentation bugs in Block 1 and Block 2.
Reads broken file, fixes both blocks, writes corrected output.
"""
import sys
import re
from pathlib import Path

VIEWS_PATH = Path(r"C:\Users\user\Desktop\programos\sellcar\apps\listings\views.py")

# ─── BLOCK 1: listing_create() step 6/7 GET handler ───
BROKEN_1 = """        elif step == 6:
                    initial = {}
                    if current_draft:
                        initial = {'description': current_draft.description}
                    form = Step6DescriptionForm(initial=initial)
                elif step == 7:
                    user_phone = ''
                    if hasattr(request.user, 'profile') and request.user.profile.phone_number:
                        user_phone = request.user.profile.phone_number
        
                    initial = {}
                    if current_draft:
                        initial = {
                            'country': current_draft.country or 'US',
                            'city': current_draft.city if current_draft.city != '\u2014' else '',
                            'postal_code': current_draft.postal_code,
                            'address': current_draft.address,
                            'hide_exact_address': current_draft.hide_exact_address,
                            'phone': user_phone,
                            'email': request.user.email,
                            'agree_terms': False,
                        }
                    form = Step7ContactForm(initial=initial)
                else:
                    return redirect('/create/?step=1')"""

FIXED_1 = """        elif step == 6:
            initial = {}
            if current_draft:
                initial = {'description': current_draft.description}
            form = Step6DescriptionForm(initial=initial)
        elif step == 7:
            user_phone = ''
            if hasattr(request.user, 'profile') and request.user.profile.phone_number:
                user_phone = request.user.profile.phone_number

            initial = {}
            if current_draft:
                initial = {
                    'country': current_draft.country or 'US',
                    'city': current_draft.city if current_draft.city != '\u2014' else '',
                    'postal_code': current_draft.postal_code,
                    'address': current_draft.address,
                    'hide_exact_address': current_draft.hide_exact_address,
                    'phone': user_phone,
                    'email': request.user.email,
                    'agree_terms': False,
                }
            form = Step7ContactForm(initial=initial)
        else:
            return redirect('/create/?step=1')"""

# ─── BLOCK 2: _render_edit_step() step 6/7 ───
BROKEN_2 = """    elif step == 6:
            form = Step6DescriptionForm(initial={'description': listing.description})
        elif step == 7:
            seller_phone = ''
            if hasattr(listing.seller, 'profile') and listing.seller.profile.phone_number:
                seller_phone = listing.seller.profile.phone_number
     
            form = Step7ContactForm(initial={
                'country': listing.country,
                'city': listing.city,
                'postal_code': listing.postal_code,
                'address': listing.address,
                'hide_exact_address': listing.hide_exact_address,
                'phone': seller_phone,
                'email': listing.seller.email,
                'agree_terms': True,
            })
        else:
            return redirect('listing_edit_hub', pk=listing.pk)"""

FIXED_2 = """    elif step == 6:
        form = Step6DescriptionForm(initial={'description': listing.description})
    elif step == 7:
        seller_phone = ''
        if hasattr(listing.seller, 'profile') and listing.seller.profile.phone_number:
            seller_phone = listing.seller.profile.phone_number

        form = Step7ContactForm(initial={
            'country': listing.country,
            'city': listing.city,
            'postal_code': listing.postal_code,
            'address': listing.address,
            'hide_exact_address': listing.hide_exact_address,
            'phone': seller_phone,
            'email': listing.seller.email,
            'agree_terms': True,
        })
    else:
        return redirect('listing_edit_hub', pk=listing.pk)"""


def main():
    if not VIEWS_PATH.exists():
        print(f"[ERROR] File not found: {VIEWS_PATH}")
        sys.exit(1)
    
    text = VIEWS_PATH.read_text(encoding='utf-8')
    
    # Backup
    backup = VIEWS_PATH.with_suffix('.py.bak2')
    backup.write_text(text, encoding='utf-8')
    print(f"[OK] Backup saved: {backup}")
    
    # Try exact match first, then flexible match
    changed_1 = False
    changed_2 = False
    
    if BROKEN_1 in text:
        text = text.replace(BROKEN_1, FIXED_1)
        changed_1 = True
        print("[OK] Block 1 fixed (exact match)")
    else:
        # Try flexible match — collapse all whitespace differences
        # Match by finding key markers
        m = re.search(
            r"        elif step == 6:\s*\n\s+initial = \{\}\s*\n\s+if current_draft:\s*\n\s+initial = \{'description': current_draft\.description\}\s*\n\s+form = Step6DescriptionForm\(initial=initial\)\s*\n\s+elif step == 7:.*?\s+else:\s*\n\s+return redirect\('/create/\?step=1'\)",
            text,
            re.DOTALL
        )
        if m:
            text = text[:m.start()] + FIXED_1 + text[m.end():]
            changed_1 = True
            print("[OK] Block 1 fixed (regex match)")
        else:
            print("[WARN] Block 1 not found — already fixed or different format")
    
    if BROKEN_2 in text:
        text = text.replace(BROKEN_2, FIXED_2)
        changed_2 = True
        print("[OK] Block 2 fixed (exact match)")
    else:
        m = re.search(
            r"    elif step == 6:\s*\n\s+form = Step6DescriptionForm\(initial=\{'description': listing\.description\}\)\s*\n\s+elif step == 7:.*?\s+else:\s*\n\s+return redirect\('listing_edit_hub', pk=listing\.pk\)",
            text,
            re.DOTALL
        )
        if m:
            text = text[:m.start()] + FIXED_2 + text[m.end():]
            changed_2 = True
            print("[OK] Block 2 fixed (regex match)")
        else:
            print("[WARN] Block 2 not found — already fixed or different format")
    
    # Write back
    VIEWS_PATH.write_text(text, encoding='utf-8')
    print(f"[OK] File saved: {VIEWS_PATH}")
    
    # Validate Python syntax
    import ast
    try:
        ast.parse(text)
        print("[OK] Python syntax is VALID")
    except SyntaxError as e:
        print(f"[ERROR] Python syntax error at line {e.lineno}: {e.msg}")
        sys.exit(1)
    
    print()
    print("="*50)
    print("DONE! Now run: python manage.py check")
    print("="*50)

if __name__ == '__main__':
    main()