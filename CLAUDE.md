# AutoLeft (sellcar)
Django vehicle marketplace, Lithuanian-first. PRODUCTION server — be careful.

## Environment
- This IS the live production server (/root/autoleft), PostgreSQL, gunicorn via /run/gunicorn.sock, nginx
- After backend changes: systemctl restart gunicorn
- You may run migrations, collectstatic and systemctl restart gunicorn yourself without asking; report what you did at the end
- Never run destructive DB commands (DROP, DELETE without WHERE, flush) — always ask first
- deploy-agent.sh exists for snapshot deploys (last_good rollback)

## Conventions
- i18n: all templates {% load i18n %} + {% trans %}; views use gettext as _; models use gettext_lazy. Msgids written in Lithuanian (LT is source language). Single quotes inside HTML attributes
- Prices: step=1, |floatformat:0, "$" suffix; months 01-12; dates m/Y
- Internal links: {% url 'xxx' %}?{{ request.GET.urlencode }} to preserve filters
- Frontend: Alpine.js + Tailwind
- Single Listing table for most categories via ?category= filter; trucks have separate TruckBrand/TruckModel tables
- Search panel partials live in templates/listings/partials/ (search_rail.html, search_panel.html, panel_*.html)

## Workflow
- Commit as you go: small logical commits after each meaningful step, Conventional Commits format (feat/fix/chore...), then push
- Test accounts: admin romasm3@gmail.com, buyer romasm333@gmail.com
