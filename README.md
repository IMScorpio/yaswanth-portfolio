# Yaswanth Battina portfolio

Responsive static portfolio with a blog, privacy notice, SEO metadata, and a server backed aggregate page view counter.

## Edit content

- Main portfolio details and project cards are in the `CONFIG` object near the top of the script in `index.html`.
- Add or edit posts in `articles/`, with one standalone HTML file per article. Update the article card and BlogPosting JSON-LD in `blog.html`, and add its canonical URL to `sitemap.xml`. There is no public blog editor or upload button: visitors can only read published posts.
- For a new post, copy an existing article page and give it a unique slug, title, description, canonical URL, publication date, and accurate `BlogPosting` JSON-LD. Add a card to `blog.html`; update the homepage `NOTES` preview only if you want to feature it. Commit/deploy the files through the private site repository. Keep drafts in your private working copy and do not add credentials or unpublished personal information to the public site.
- Review `privacy.html` whenever the site's services or data practices change.

## Local preview and verification

- Install packages: `npm install`
- Unit checks: `npm test`
- Responsive browser check: install Python Playwright and Chromium, then run `python responsive_check.py`.
- The global visit total works after deployment with the configured server function. In a local static preview, the count stays as an em dash without showing an error message; the rest of the site works normally.

## Deploy to Netlify

Connect this folder to the existing Netlify site or deploy it as a new site. `netlify.toml` configures the static publish folder and the `netlify/functions` directory. Netlify builds the `views.mjs` function and provisions site-wide Blobs access in the function runtime. The counter stores one aggregate number only; no visitor identifiers are written by the function.

## SEO and privacy notes

The home, blog, and privacy pages include page titles and descriptions; the blog includes article metadata and structured data. `robots.txt` and `sitemap.xml` point crawlers to the public pages. Search indexing and monetization depend on site content, publishing quality, audience, and platform approval; this project does not guarantee rankings or earnings.

The privacy notice describes the current implementation and third-party services. It is a practical transparency measure, not a certification of compliance in every country. Review it against the site's actual hosting and font service settings before publishing.
