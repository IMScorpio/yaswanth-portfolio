# Real-browser responsive check. Run: pip install playwright && playwright install chromium && python3 responsive_check.py
from playwright.sync_api import sync_playwright
import sys
URL="file://"+__import__("os").path.abspath("index.html")
SIZES=[(320,640),(390,844),(768,1024),(1024,768),(1440,900)]
fail=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h in SIZES:
        pg=b.new_page(viewport={"width":w,"height":h});pg.goto(URL);pg.wait_for_timeout(300)
        r=pg.evaluate("""()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,
         small:[...document.querySelectorAll('a,button')].filter(e=>e.offsetParent&&e.getBoundingClientRect().height<36).map(e=>e.textContent.trim())})""")
        if r["sw"]>r["cw"]:fail.append(f"{w}px: horizontal scroll")
        if r["small"]:fail.append(f"{w}px: small tap targets {r['small']}")
        if w<=760:
            if not pg.is_visible("#mb"):fail.append(f"{w}px: menu button hidden")
            pg.click("#mb");
            if not pg.is_visible("#nl a.btn"):fail.append(f"{w}px: CTA not reachable in menu")
            pg.click("#nl a[href='#contact']");pg.wait_for_timeout(500)
            if pg.is_visible("#nl"):fail.append(f"{w}px: menu stays open")
        else:
            if pg.is_visible("#mb"):fail.append(f"{w}px: menu button shown on wide screen")
            if not pg.is_visible("nav a.btn"):fail.append(f"{w}px: CTA hidden")
        cols=pg.evaluate("getComputedStyle(document.getElementById('idc')).gridTemplateColumns.split(' ').length")
        if cols!=(3 if w>=700 else 1):fail.append(f"{w}px: card columns={cols}")
    for page in ["blog.html", "privacy.html"]:
        for w,h in SIZES:
            pg=b.new_page(viewport={"width":w,"height":h});pg.goto("file://"+__import__("os").path.abspath(page));pg.wait_for_timeout(150)
            r=pg.evaluate("""()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,main:!!document.querySelector('main'),description:!!document.querySelector('meta[name=description]'),wide:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(0,3).map(e=>e.tagName.toLowerCase()+' '+e.innerText.trim().slice(0,50))})""")
            if r["sw"]>r["cw"]:fail.append(f"{page} at {w}px: horizontal scroll {r['wide']}")
            if not r["main"] or not r["description"]:fail.append(f"{page} at {w}px: missing main content or SEO description")
            pg.close()
    b.close()
print("FAIL:\n"+"\n".join(fail) if fail else "ALL RESPONSIVE CHECKS PASSED");sys.exit(1 if fail else 0)
