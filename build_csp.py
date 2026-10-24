"""Regenerate the Content-Security-Policy line in _headers.

Run after ANY change to an inline <script> on any page:
    python build_csp.py
It hashes every inline script (JSON-LD excluded) in the deployable pages
and rewrites the CSP line under "/*" in _headers. Not deployed (leave it
out of the publish copy, like build_playbook.py).

HEADER_NAME is Report-Only while violations are being checked. Switch it to
"Content-Security-Policy" to enforce, only after the browser console shows
no CSP reports on every page (see CLAUDE.md).
"""
import base64, glob, hashlib, re, sys

HEADER_NAME = "Content-Security-Policy-Report-Only"
SKIP = ("reports/", "research_notes/", ".claude/")

HOSTS = {
    "script-src": [
        "https://www.googletagmanager.com",
        "https://*.clarity.ms",
        "https://static.cloudflareinsights.com",
        "https://www.instagram.com",
    ],
    "connect-src": [
        "https://*.google-analytics.com",
        "https://*.analytics.google.com",
        "https://*.googletagmanager.com",
        "https://*.clarity.ms",
        "https://cloudflareinsights.com",
        "https://formsubmit.co",
    ],
    "img-src": [
        "data:",
        "https://*.google-analytics.com",
        "https://*.googletagmanager.com",
        "https://*.clarity.ms",
        "https://assets.simplotel.com",
        "https://*.cdninstagram.com",
        "https://*.fbcdn.net",
    ],
    "media-src": ["https://cdn1.simplotel.com"],
    "frame-src": ["https://www.youtube-nocookie.com", "https://www.instagram.com"],
    "form-action": ["https://formsubmit.co"],
}


def inline_hashes():
    hashes = set()
    pages = [p for p in glob.glob("**/*.html", recursive=True) if not p.replace("\\", "/").startswith(SKIP)]
    for page in pages:
        html = open(page, encoding="utf-8").read()
        for m in re.finditer(r"<script(\s[^>]*)?>(.*?)</script>", html, re.S):
            attrs, body = m.group(1) or "", m.group(2)
            if "src=" in attrs or "ld+json" in attrs:
                continue
            digest = hashlib.sha256(body.encode("utf-8")).digest()
            hashes.add("'sha256-" + base64.b64encode(digest).decode() + "'")
    return sorted(hashes), len(pages)


def policy(hashes):
    parts = [
        "default-src 'self'",
        "script-src 'self' " + " ".join(hashes + HOSTS["script-src"]),
        "style-src 'self' 'unsafe-inline'",
        "font-src 'self'",
        "img-src 'self' " + " ".join(HOSTS["img-src"]),
        "media-src 'self' " + " ".join(HOSTS["media-src"]),
        "connect-src 'self' " + " ".join(HOSTS["connect-src"]),
        "frame-src " + " ".join(HOSTS["frame-src"]),
        "form-action 'self' " + " ".join(HOSTS["form-action"]),
        "object-src 'none'",
        "base-uri 'self'",
        "frame-ancestors 'self'",
    ]
    return "; ".join(parts)


def main():
    hashes, n = inline_hashes()
    line = "  " + HEADER_NAME + ": " + policy(hashes)
    if len(line) > 2000:
        sys.exit("CSP line is %d characters; Cloudflare Pages allows 2,000 per _headers line." % len(line))
    text = open("_headers", encoding="utf-8").read()
    text = re.sub(r"\n  Content-Security-Policy(-Report-Only)?:[^\n]*", "", text)
    text = text.replace("/*\n", "/*\n" + line + "\n", 1)
    open("_headers", "w", encoding="utf-8", newline="\n").write(text)
    print("%d pages, %d inline script hashes, line length %d" % (n, len(hashes), len(line)))


if __name__ == "__main__":
    main()
