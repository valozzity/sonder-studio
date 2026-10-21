#!/usr/bin/env bash
#
# Package a clean Mailchimp import zip from a show's working folder.
#
# Mailchimp's "Import zip" picks an HTML file from the archive. If more than one
# .html is present (blog_body.html, rsvp_page.html tend to pile up next to the
# email), it can load the wrong one and ship an unstyled email. This script
# sidesteps that entirely: it copies ONLY index.html + the images index.html
# references into a clean temp dir, then zips that. The result can only ever
# load the styled email.
#
# Usage:
#   package_mailchimp_zip.sh <working-folder> <output.zip>
#
# Example:
#   package_mailchimp_zip.sh "shows/euphorbia/closer-look" \
#                            "shows/euphorbia/euphorbia_closer_look_MAILCHIMP.zip"

set -euo pipefail

SRC="${1:-}"
OUT="${2:-}"

if [[ -z "$SRC" || -z "$OUT" ]]; then
  echo "Usage: package_mailchimp_zip.sh <working-folder> <output.zip>" >&2
  exit 1
fi

if [[ ! -f "$SRC/index.html" ]]; then
  echo "Error: no index.html found in '$SRC'." >&2
  echo "The email must be named index.html so Mailchimp loads it." >&2
  exit 1
fi

# Parse the image files index.html actually references (src="...jpg|png|gif|webp"),
# so we include exactly what the email needs — no stray assets, no other HTML.
IMAGES=$(grep -oE 'src="[^"]+\.(jpg|jpeg|png|gif|webp)"' "$SRC/index.html" \
         | sed -E 's/^src="//; s/"$//' \
         | sort -u)

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

cp "$SRC/index.html" "$STAGE/"

missing=0
for img in $IMAGES; do
  # Only handle local relative images; skip absolute URLs (already hosted).
  if [[ "$img" == http* ]]; then
    continue
  fi
  if [[ -f "$SRC/$img" ]]; then
    # Flatten into the zip root next to index.html (relative src stays valid).
    cp "$SRC/$img" "$STAGE/$(basename "$img")"
  else
    echo "Warning: index.html references '$img' but it's missing from '$SRC'." >&2
    missing=1
  fi
done

# Resolve the output path to an absolute location before we cd into the stage.
rm -f "$OUT"
mkdir -p "$(dirname "$OUT")"
OUT_ABS="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"

# Build the zip from the clean stage. -X strips extra macOS attributes; the
# excludes drop any junk that slipped in.
( cd "$STAGE" && zip -X -r "$OUT_ABS" . -x '*.DS_Store' -x '__MACOSX*' >/dev/null )

echo "Built: $OUT"
echo "--- contents ---"
unzip -l "$OUT"

html_count=$(unzip -l "$OUT" | grep -cE '\.html$' || true)
if [[ "$html_count" -ne 1 ]]; then
  echo "ERROR: zip contains $html_count .html files (must be exactly 1)." >&2
  exit 1
fi
if [[ "$missing" -eq 1 ]]; then
  echo "NOTE: some referenced images were missing (see warnings above)." >&2
fi
echo "OK: exactly one HTML file. Safe to import into Mailchimp."
