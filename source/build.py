#!/usr/bin/env python3
"""Builds the static JCW Solutions site from page fragments.

Usage:  python3 build.py            # draft build (placeholders allowed)
        python3 build.py --release  # fails if any [TO CONFIRM] marker remains
"""
import pathlib, re, sys, datetime
import config as C

SRC = pathlib.Path(__file__).parent / "pages"
OUT = pathlib.Path(__file__).resolve().parent.parent  # repository root, which GitHub Pages serves

PAGES = [
    # (fragment, output path, title, description, nav key)
    ("home.html", "index.html", "JCW Solutions — Business & technology analysis, and privacy-first apps",
     "JCW Solutions helps organisations turn complex business and technology challenges into clear requirements, workable solutions and reliable delivery — and builds privacy-first apps for iPhone.", "home"),
    ("freeday.html", "freeday/index.html", "Freeday — Private personal finance for iPhone",
     "Freeday is a privacy-conscious personal finance app for iPhone from JCW Solutions, built around reliable financial records that stay under your control.", "freeday"),
    ("freeday-privacy.html", "freeday/privacy/index.html", "Freeday Privacy Policy — JCW Solutions",
     "How the Freeday app handles your financial data, including data shared from Apple Wallet through FinanceKit.", "freeday"),
    ("freeday-support.html", "freeday/support/index.html", "Freeday Support — JCW Solutions",
     "Get help with Freeday, manage the data you share, and contact support.", "freeday"),
    ("site-privacy.html", "privacy/index.html", "Website Privacy Notice — JCW Solutions",
     "How the jcw.solutions website handles information about visitors.", "privacy"),
    ("404.html", "404.html", "Page not found — JCW Solutions", "Page not found.", ""),
]

NAV = [("home", "/", "Home"), ("services", "/#services", "Consultancy"),
       ("products", "/#products", "Products"), ("freeday", "/freeday/", "Freeday"),
       ("contact", "/#contact", "Contact")]


def header(active):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a>'
        for key, href, label in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
  <a class="brand" href="/" aria-label="JCW Solutions home"><span class="brand-mark" aria-hidden="true">JCW</span>JCW Solutions</a>
  <nav class="nav" aria-label="Main">{links}</nav>
</div></header>'''


def footer():
    year = datetime.date.today().year
    return f'''<footer class="site-footer"><div class="wrap">
  <div class="cols">
    <div>
      <p><strong>JCW Solutions</strong> — business and technology analysis, and privacy-first apps. Based in the UK.</p>
      <p>&copy; {year} JCW Solutions, a trading name of {C.LEGAL_ENTITY}. {C.COMPANY_DETAILS}</p>
      <p>Apple, iPhone, Apple Wallet, Apple Intelligence and iCloud are trademarks of Apple Inc.</p>
    </div>
    <div><h4>Freeday</h4><ul>
      <li><a href="/freeday/">About Freeday</a></li>
      <li><a href="/freeday/privacy/">Freeday Privacy Policy</a></li>
      <li><a href="/freeday/support/">Freeday Support</a></li>
    </ul></div>
    <div><h4>Company</h4><ul>
      <li><a href="/#services">Consultancy</a></li>
      <li><a href="/#contact">Contact</a></li>
      <li><a href="/privacy/">Website Privacy</a></li>
    </ul></div>
  </div>
</div></footer>'''


def render(fragment, title, desc, active, path):
    body = (SRC / fragment).read_text()
    for key in dir(C):
        if key.isupper():
            body = body.replace("{{" + key + "}}", str(getattr(C, key)))
    for key, val in C.FACTS.items():
        body = body.replace("{{todo_" + key + "}}", val)
    missing = re.findall(r"\{\{[^}]+\}\}", body)
    if missing:
        sys.exit(f"{fragment}: unknown placeholders {missing}")
    canonical = C.SITE_URL + "/" + path.replace("index.html", "")
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/site.js" defer></script>
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''


def main():
    release = "--release" in sys.argv
    leftovers = {}
    for fragment, out, title, desc, active in PAGES:
        html = render(fragment, title, desc, active, out)
        found = re.findall(r"\[TO CONFIRM: ([^\]]+)\]", html)
        if found:
            leftovers[out] = sorted(set(found))
        dest = OUT / out
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html)
    urls = "".join(f"  <url><loc>{C.SITE_URL}/{p[1].replace('index.html','')}</loc></url>\n"
                   for p in PAGES if p[1] != "404.html")
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /source/\nSitemap: {C.SITE_URL}/sitemap.xml\n")
    (OUT / "CNAME").write_text("jcw.solutions\n")
    (OUT / ".nojekyll").write_text("")
    for page, items in leftovers.items():
        print(f"{page}:")
        for i in items:
            print(f"   - {i}")
    total = sum(len(v) for v in leftovers.values())
    print(f"\nBuilt {len(PAGES)} pages. Unique placeholders remaining per page total: {total}")
    if release and leftovers:
        sys.exit("Release build blocked: fill every [TO CONFIRM] first.")


if __name__ == "__main__":
    main()
