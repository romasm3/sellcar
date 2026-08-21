"""Elementų sąrašas iš viršaus į apačią — etalonui ir mums, ta pačia metodika."""
from playwright.sync_api import sync_playwright
import json, sys

UAD='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
UAM='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'

# Renkam tik „prasmingus" blokus: matomus, su turiniu, ne gilesnius nei N lygių
SCAN = """(maxDepth) => {
  const out = [];
  const seen = new Set();
  const skip = /^(script|style|svg|path|circle|rect|br|noscript|template)$/i;
  const walk = (el, depth) => {
    if (depth > maxDepth) return;
    for (const c of el.children) {
      if (skip.test(c.tagName)) continue;
      const s = getComputedStyle(c);
      if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') continue;
      const r = c.getBoundingClientRect();
      if (r.height < 6 || r.width < 6) { walk(c, depth + 1); continue; }
      const txt = (c.innerText || '').replace(/\\s+/g, ' ').trim();
      const tag = c.tagName.toLowerCase();
      const cls = (c.className || '').toString().trim().split(/\\s+/).slice(0, 3).join('.');
      const key = tag + '|' + cls + '|' + Math.round(r.top) + '|' + Math.round(r.height);
      if (!seen.has(key)) {
        seen.add(key);
        out.push({y: Math.round(r.top + window.scrollY), h: Math.round(r.height),
                  w: Math.round(r.width), tag, cls: cls.slice(0, 40),
                  t: txt.slice(0, 90), vaikų: c.children.length});
      }
      walk(c, depth + 1);
    }
  };
  walk(document.body, 0);
  return out.sort((a, b) => a.y - b.y || a.h - b.h);
}"""

def scan(pg, depth=4):
    pg.wait_for_timeout(2500)
    for _ in range(6):
        pg.mouse.wheel(0, 1200); pg.wait_for_timeout(250)
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500)
    return pg.evaluate(SCAN, depth)

def run(tasks, out_path):
    data = {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox"])
        for name, url, mobile, insecure in tasks:
            ctx = b.new_context(viewport={"width": 390 if mobile else 1440, "height": 900},
                                user_agent=UAM if mobile else UAD,
                                is_mobile=mobile, has_touch=mobile,
                                ignore_https_errors=insecure, locale="lt-LT")
            pg = ctx.new_page()
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=60000)
                data[name] = scan(pg)
                print(f"{name}: {len(data[name])} elementų", flush=True)
            except Exception as e:
                data[name] = [{"klaida": str(e)[:120]}]
                print(f"{name}: KLAIDA {str(e)[:80]}", flush=True)
            ctx.close()
        b.close()
    json.dump(data, open(out_path, "w"), ensure_ascii=False, indent=1)
