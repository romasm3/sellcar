#!/usr/bin/env python3
"""
One-shot patcher for AutoLeft:
  1. Hides draft listings from the dashboard (my_listings view).
  2. Adds the cleanup_abandoned_drafts management command.

Run from project root (where manage.py is):
    python patch_drafts.py
Then:
    sudo systemctl restart gunicorn
"""
import ast
import os
import re
import sys

VIEWS = 'apps/listings/views.py'


def patch_views():
    if not os.path.exists(VIEWS):
        print(f"ERROR: {VIEWS} not found. Run this from the project root (where manage.py is).")
        sys.exit(1)

    src = open(VIEWS, encoding='utf-8').read()
    marker = 'def my_listings(request):'
    if marker not in src:
        print("ERROR: my_listings() not found in views.py")
        sys.exit(1)

    start = src.index(marker)
    m = re.search(r'\n@\w|\ndef ', src[start + len(marker):])
    end = start + len(marker) + m.start() if m else len(src)

    func = src[start:end]
    new = func
    # 1. inactive list + inactive_count: drop drafts (2 occurrences inside my_listings)
    new = new.replace("status__in=['expired', 'draft']", "status='expired'")
    # 2. "All" tab: exclude drafts from the list...
    new = new.replace("        listings = base_qs\n",
                      "        listings = base_qs.exclude(status='draft')\n")
    # 3. ...and from the all_count number
    new = new.replace("all_count = base_qs.count()",
                      "all_count = base_qs.exclude(status='draft').count()")

    if new == func:
        print("NOTE: views.py already patched (no changes made).")
        return

    candidate = src[:start] + new + src[end:]
    ast.parse(candidate)  # validate — raises SyntaxError if broken
    with open(VIEWS, 'w', encoding='utf-8') as f:
        f.write(candidate)
    print("OK: views.py my_listings patched (drafts hidden from dashboard).")


def write_command():
    d = 'apps/listings/management/commands'
    os.makedirs(d, exist_ok=True)
    for p in ('apps/listings/management/__init__.py', d + '/__init__.py'):
        if not os.path.exists(p):
            open(p, 'w').close()

    code = '''from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.listings.models import Listing


class Command(BaseCommand):
    help = "Delete abandoned draft listings (status='draft') not updated in N days."

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=7,
                            help='Delete drafts not updated in this many days (default 7).')
        parser.add_argument('--dry-run', action='store_true',
                            help='Show what would be deleted without deleting.')

    def handle(self, *args, **options):
        days = options['days']
        cutoff = timezone.now() - timedelta(days=days)
        qs = Listing.objects.filter(status='draft', updated_at__lt=cutoff)
        count = qs.count()
        if count == 0:
            self.stdout.write(f"No abandoned drafts older than {days}d.")
            return
        if options['dry_run']:
            self.stdout.write(f"[dry-run] {count} draft(s) would be deleted:")
            for d in qs.order_by('updated_at')[:50]:
                self.stdout.write(f"  #{d.pk} '{d.title}' (updated {d.updated_at:%Y-%m-%d})")
            return
        qs.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} abandoned draft(s)."))
'''
    path = d + '/cleanup_abandoned_drafts.py'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"OK: {path} created.")


if __name__ == '__main__':
    patch_views()
    write_command()
    print("\nDone. Now run:  sudo systemctl restart gunicorn")
