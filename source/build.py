#!/usr/bin/env python3
"""Builds the static JCW Solutions site from page fragments.

Usage:  python3 build.py            # draft build (placeholders allowed)
        python3 build.py --release  # fails if any [TO CONFIRM] marker remains
"""
import pathlib, re, sys, datetime

MARK = '<svg class="brand-mark" viewBox="0 0 512 512" aria-hidden="true" focusable="false"><rect width="512" height="512" rx="81.92" class="tile"/><path d="M159.76448 473.5488Q146.11455999999998 473.5488 137.52832 466.28352Q128.94208 459.01824 128.94208 447.1296Q128.94208 438.3232 134.00576 432.59904Q139.06944 426.87488 146.99519999999998 426.87488Q154.48064 426.87488 157.56288 431.27808000000005Q160.64512 435.68128 162.62655999999998 441.40544Q164.608 447.1296 167.24992 451.53279999999995Q169.89184 455.936 175.61599999999999 455.936Q183.98208 455.936 188.38528 446.24896Q192.78848 436.56192 192.78848 418.94912V90.91072000000003Q192.78848 81.66399999999999 189.9264 78.58176Q187.06432 75.49952000000002 177.8176 73.73824000000002L167.69024 71.97696000000002Q161.96608 70.656 161.96608 66.69312000000002Q161.96608 61.84960000000001 168.57088 61.84960000000001H248.2688Q254.8736 61.84960000000001 254.8736 66.69312000000002Q254.8736 70.656 249.14944 71.97696000000002L239.02208 73.73824000000002Q229.77535999999998 75.49952000000002 226.91328 78.58176Q224.0512 81.66399999999999 224.0512 90.91072000000003V359.50592Q224.0512 412.34432 206.87872 442.94656Q189.70623999999998 473.5488 159.76448 473.5488Z" class="j"/><circle cx="358.40" cy="340.48" r="38.40" class="stop"/></svg>'
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

NAV = [("services", "/#services", "Consultancy"), ("about", "/#about", "About"),
       ("freeday", "/freeday/", "Freeday"), ("contact", "/#contact", "Contact")]


def header(active):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a>'
        for key, href, label in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
  <a class="brand" href="/" aria-label="JCW Solutions home">{MARK}<span>JCW <em>Solutions</em></span></a>
  <nav class="nav" aria-label="Main">{links}</nav>
</div></header>'''


def footer():
    year = datetime.date.today().year
    return f'''<footer class="site-footer"><div class="wrap">
  <div class="cols">
    <div>
      <a class="brand" href="/" aria-label="JCW Solutions home">{MARK}<span>JCW <em>Solutions</em></span></a>
      <p class="tagline">Clear requirements. Workable solutions. Reliable delivery<span class="dot">.</span></p>
      <p>Independent UK business and technical analysis, and privacy-conscious apps.<br><a href="mailto:josh@jcw.solutions">josh@jcw.solutions</a></p>
    </div>
    <div><h4>Freeday</h4><ul>
      <li><a href="/freeday/">About Freeday</a></li>
      <li><a href="/freeday/privacy/">Freeday privacy policy</a></li>
      <li><a href="/freeday/support/">Freeday support</a></li>
    </ul></div>
    <div><h4>Company</h4><ul>
      <li><a href="/#services">Consultancy</a></li>
      <li><a href="/#about">About</a></li>
      <li><a href="/#contact">Contact</a></li>
      <li><a href="/privacy/">Website privacy</a></li>
    </ul></div>
  </div>
  <p class="legal">&copy; {year} JCW Solutions is a trading name of {C.LEGAL_ENTITY}, registered in England &amp; Wales, company no. {C.COMPANY_NUMBER}. Registered office: {C.REGISTERED_OFFICE}.<br>Apple, iPhone, Apple Wallet, Apple Intelligence and iCloud are trademarks of Apple Inc.</p>
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
<meta name="theme-color" content="#F5F1E8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#111A2B" media="(prefers-color-scheme: dark)">
<link rel="preload" href="/assets/fonts/instrument-serif.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/site.js" defer></script>
</head>
<body data-section="{active or "site"}">
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
