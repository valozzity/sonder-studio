"""
Pull everything an email needs out of a Sonder pre-catalogue PDF.

    python3 scripts/extract_catalogue.py <catalogue.pdf> <out-folder>

Writes into <out-folder>:
  catalogue.json        show text, artist bio, and one entry per work
  cover.jpg             page 1 rendered (show title is part of the cover art)
  wordmark.png          the black SONDER wordmark from a work page
  works/<slug>.jpg      the work photo from each work page
  works/<slug>-detail.jpg  the close-up page that follows it, when there is one

Layout this expects (the Euphorbia catalogue): p1 cover, p2 press text,
then work pages ("Title, Year / medium / in / cm / $price") that may be
followed by a text-free detail page, then a bio page and a contact page.
"""

import io
import json
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image

PRICE = re.compile(r"^\$[\d,]+")
TITLE_YEAR = re.compile(r"^(?P<title>.+?),\s*(?P<year>\d{4}(?:\s*[-–]\s*\d{4})?)$")


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def page_lines(page):
    return [l.strip() for l in page.get_text().splitlines() if l.strip()]


def largest_image(doc, page):
    best = None
    for img in page.get_images(full=True):
        xref = img[0]
        w, h = img[2], img[3]
        if best is None or w * h > best[1] * best[2]:
            best = (xref, w, h)
    if not best:
        return None
    raw = doc.extract_image(best[0])
    return Image.open(io.BytesIO(raw["image"])).convert("RGB")


def save_jpg(im, path, max_w=1200, q=84):
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    im.save(path, "JPEG", quality=q, progressive=True, optimize=True)


def parse_work(lines):
    m = TITLE_YEAR.match(lines[0])
    if not m:
        return None
    work = {"title": m["title"], "year": m["year"], "medium": lines[1] if len(lines) > 1 else ""}
    dims = [l for l in lines[2:] if not PRICE.match(l)]
    work["dims_in"] = next((d for d in dims if " in" in d or d.endswith("in")), "")
    work["dims_cm"] = next((d for d in dims if "cm" in d), "")
    price = next((l for l in lines if PRICE.match(l)), "")
    work["price"] = price
    return work


def main(pdf, out):
    out = Path(out)
    (out / "works").mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf)

    # Cover: render the whole page; the show's display title is baked in.
    cover = doc[0].get_pixmap(matrix=fitz.Matrix(2, 2))
    Image.frombytes("RGB", (cover.width, cover.height), cover.samples).save(out / "cover.jpg", quality=86)

    data = {"source": str(pdf), "press_text": [], "bio": [], "works": []}
    data["press_text"] = page_lines(doc[1])

    wordmark_done = False
    for i in range(2, len(doc)):
        page = doc[i]
        lines = page_lines(page)
        work = parse_work(lines) if lines else None

        if work:
            slug = slugify(work["title"])
            work["slug"] = slug
            work["page"] = i + 1
            im = largest_image(doc, page)
            if im:
                save_jpg(im, out / "works" / f"{slug}.jpg")
                work["image"] = f"works/{slug}.jpg"
            # The next page is the close-up when it carries no text.
            if i + 1 < len(doc) and not page_lines(doc[i + 1]):
                det = largest_image(doc, doc[i + 1])
                if det:
                    save_jpg(det, out / "works" / f"{slug}-detail.jpg")
                    work["detail_image"] = f"works/{slug}-detail.jpg"
            data["works"].append(work)

            if not wordmark_done:
                # Wordmark sits top-left of every work page.
                r = page.rect
                clip = fitz.Rect(0, 0, r.width * 0.2, r.height * 0.09)
                pix = page.get_pixmap(matrix=fitz.Matrix(8, 8), clip=clip)
                wm = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                bbox = Image.eval(wm.convert("L"), lambda v: 255 - v).getbbox()
                wm.crop(bbox).save(out / "wordmark.png")
                wordmark_done = True
        elif lines and "(b." in lines[0]:
            data["bio"] = lines

    with open(out / "catalogue.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"{len(data['works'])} works -> {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
