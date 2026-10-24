# jcw.solutions

Website for JCW Solutions (a trading name of JCW Digital Ltd), served by GitHub Pages at https://jcw.solutions.

## How it's organised

| Path | What it is |
| --- | --- |
| `index.html`, `freeday/`, `privacy/`, `404.html` | The built pages GitHub Pages serves. Don't edit these by hand. |
| `assets/` | Shared stylesheet, Freeday icon and app screenshots (WebP, light and dark). |
| `source/pages/` | Page templates. Edit these. |
| `source/config.py` | Details used on several pages: company name, number, registered office, emails, policy date. |
| `source/build.py` | Builds the pages from the templates into the repository root. |

## Updating the site

1. Edit a template in `source/pages/` or a value in `source/config.py`.
2. Run `python3 source/build.py --release`. It refuses to build if any `[TO CONFIRM]` placeholder is left.
3. Commit and push. GitHub Pages publishes within a few minutes.

## Screenshots

The Freeday screenshots in `assets/shots/` come from the app's demo mode (fictional data). The `ci/site-screenshots` branch in the `freeday-financekit` repo builds the app on a GitHub macOS runner and commits fresh screenshots to its `site-screenshots-output` branch. Convert them to 600×1304 WebP and replace the files in `assets/shots/`.

## Hosting

- DNS: GoDaddy. Four A records for `@` point to GitHub Pages (185.199.108–111.153), and `www` is a CNAME to `jcwsolutions.github.io`.
- HTTPS is enforced in the repository's Pages settings.
- The site sets no cookies and loads nothing from third parties, as the website privacy notice states. Keep it that way, or update the notice.
