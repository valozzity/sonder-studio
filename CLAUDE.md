# Gallery Sonder studio

This folder builds Gallery Sonder's show emails (Mailchimp) and website content (Prismic). The person working here is Josh at Gallery Sonder. He's new to Claude Code, so explain in plain language and avoid jargon.

## Publishing: Josh publishes by hand, always

- **Never publish anything to the live website.** All Prismic writes (create_document, update_document) go into a Release as drafts. Josh reviews the release in Prismic and publishes it himself, by hand, in the Prismic dashboard.
- `publish_release` is blocked in `.claude/settings.json`. Don't try to get around the block. If Josh asks you to publish, tell him the release is ready and how to publish it in Prismic: open the release, review it, click Publish.
- Mailchimp works the same way: you build and package the email, and Josh imports, tests and sends it himself.
- After every Prismic write, tell Josh the release name and what changed, so he knows what he's publishing.
- Prefer creating new documents over editing live ones. Before updating an existing live page, say which page and what will change, and wait for his OK.

## Copy

- Artist and gallery copy (press text, statements, captions) is reproduced word for word. Keep the original punctuation and spacing, and don't add curly quotes. Only edit it when Josh asks.
- Work details come from the pre-catalogue PDF: title (italic), year, medium, dimensions in inches and cm, price. Use `scripts/extract_catalogue.py` to pull them.

## Emails

- Each show gets a folder: `shows/<show>/` with `catalogue/` (extracted) and one folder per email (`closer-look/`, `opening/`, ...).
- `shows/euphorbia/closer-look/` is the reference design: SONDER wordmark, the catalogue cover, the two-column info block, outlined buttons, catalogue-style work captions, the image credit line, and the standard footer.
- Every link to gallerysonder.com gets `utm_source=mailchimp&utm_medium=email&utm_campaign=<show>-<email>`, plus `utm_content=<work-slug>` on work links. Leave mailto and external links untagged.
- Package with `scripts/package_mailchimp_zip.sh <email-folder> <output>_MAILCHIMP.zip`. Never zip a whole folder by hand, because Mailchimp may pick up the wrong HTML file.
- Preview the email in a browser at desktop and phone width before packaging.
