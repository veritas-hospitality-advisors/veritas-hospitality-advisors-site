# CLAUDE.md — Veritas Hospitality Advisors Site
*Session handoff file. Update after every working session.*
*Last updated: 23 October 2026 | Branch: main*

## UPDATE 24 Oct 2026 (hosting moved to Cloudflare Pages; supersedes the GitHub Pages notes below)

**Hosting**
- The live site `https://veritashospitalityadvisors.in` (and `www`) is served by **Cloudflare Pages**, project `veritas-hospitality-advisors`, in the CLIENT's own Cloudflare account (the same account that holds the domain's DNS). GitHub Pages is no longer the host; turn it off in the repo's Settings > Pages once happy. DNS MX, SPF, DKIM, DMARC and verification records were left untouched, and SSL/TLS mode is Full.
- The project is a **direct upload, not connected to git**: pushing to GitHub does NOT update the live site. To publish, make a clean copy of the committed files (leave out `CLAUDE.md`, `build_playbook.py`, `research_notes/`, `reports/`, `_config.yml`, `CNAME`, `.claude/`, `.git`) and run `npx wrangler pages deploy <copy> --project-name veritas-hospitality-advisors --branch main` while `wrangler` is logged in to the client's account (`npx wrangler whoami` must show it). Delete any `.wrangler` cache folder in the copy first, or wrangler may use the wrong account. Then check `/perspectives/revpar` and `/sitemap.xml` on the live domain.
- `_headers` (repo root, commit 94cc533) sets HSTS, COOP, X-Frame-Options SAMEORIGIN, nosniff, Referrer-Policy, one-year immutable caching for `/fonts/`, `/images/`, `/img/`, `*.jpg`, `*.webp`, and 1 hour for `*.js`. It replaces the old "security headers parked" note. No CSP or Trusted Types: the inline GA snippet and YouTube embed would break.
- Because the repo no longer has to feed GitHub Pages, it can be made private if the owner wants (the older "repo MUST stay public" note applied only to GitHub Pages). Do not change visibility without asking.
- Still to do: a Cloudflare redirect rule from `www` to the root (both currently serve the site; canonical tags already point to the root), and deleting a stray duplicate Pages project that was created by mistake in the agency's own Cloudflare account.

**Commits**
- Commits now carry `Co-Authored-By: AISearch Global | Sydney | Australia <hello@aisearch.global>` (owner's instruction, 24 Oct 2026). This replaces the old "never add Co-Authored-By" line in the attribution section below; it still never names Claude. Push only when the owner says so.
- When a page changes, bump its `article:modified_time`, any `dateModified` in its schema, and its sitemap `lastmod` (done for 28 pages on 24 Oct, commit 581b652).

**Accessibility fixes (24 Oct 2026, commits 2842cca, ebf5c27, 5255b31)**
- Self-hosted fonts replace Google Fonts (the 'only this Google Fonts URL' rules below are superseded; the families are unchanged). Text contrast raised, in-text and footer links underlined, 24 px minimum tap targets on gallery dots, footer nav links, perspectives breadcrumb and back link, FAQ related links, home Read more and clients link. Home FAQ links and the legal contents list are underlined. `health-check.html` and `insights.html` muted and gold text darkened. A small `<style id="a11y-targets">` block before `</head>` carries the per-page overrides.
- Locked: the logo lockup. Its 'HOSPITALITY ADVISORS' line measures about 4.2:1 contrast on navy and was left alone on purpose; changing it needs the owner's sign-off.
- Known, not fixed: the dark-theme muted colour on `health-check.html` (`#5A6878`) is low contrast on dark backgrounds.
- A full scan at 375 px on 24 Oct found no unnamed buttons, unlabelled fields, missing alt text, skipped headings or sideways scroll on any page. Re-run PageSpeed on the live `founder.html` to get fresh scores (the 23 Oct run predates most fixes).

**Microsoft Clarity (added 24 Oct 2026, owner's instruction)**
- The Clarity tag (project id `z2h8l5bixi`, the Veritas project in Clarity; an earlier Bing-created id `z2h62oe5uo` was replaced on 24 Oct) is in `<head>` on all 29 pages, just before the `consent.js` line, exactly as Clarity supplied it. Keep it identical on every page; never add a second copy.
- `consent.js` calls `clarity('consent', false)` until the visitor accepts analytics, `clarity('consent', true)` on Accept, and `false` plus clearing the `_clck` / `_clsk` cookies on Decline or withdrawal. Check on the live site that Clarity sets no cookies before Accept.
- Cookie banner (24 Oct 2026, owner's instruction): buttons are 'Essential only' and 'Accept all', equal prominence; text says cookies are used only for analytics and never for marketing or advertising, WITHOUT naming the analytics tools. `legal.html` uses 'Accept all', says the hosting provider is Cloudflare, and has a generic paragraph on other optional analytics tools (cookies `_clck`, `_clsk`). It still names Google Analytics in sections 2.2, 3, 5 and 6 (client-approved earlier). The client has not yet seen the new banner and legal wording: show them before treating it as approved. No footer 'Cookie settings' link was added (the footer is locked and baked into every page).

**Performance notes (24 Oct 2026 PageSpeed, mobile)**
- The founder-page recommendations carousel script no longer reads layout at load (initial counter set directly, scroll reset deferred to the next frame) to cut a ~115 ms forced reflow. Behaviour is meant to be identical; check next/prev and the '1 of 7' counter in a real browser after any change to it.
- Legacy-JS and two extra requests come from Cloudflare itself: Web Analytics `beacon.min.js` (auto-injected) and Email Address Obfuscation `email-decode.min.js`. Turn off both in the Cloudflare dashboard if not wanted (Web Analytics is redundant with the site's own analytics; obfuscation hides the public email from crawlers and rewrites `mailto:` links, which conflicts with the canonical-email rule).
- Fonts: 5 of the 7 woff weights are discovered after the HTML (critical path about 430 ms). Only the two most important are preloaded; adding more preloads is optional and low value.

**Local script caching (24 Oct 2026)**
- `consent.js` and `lightbox.js` are cached for one year (`_headers`, immutable) and are referenced as `/consent.js?v=20261024` and `/lightbox.js?v=20261024`. When you change either file, bump the `?v=` value on every page that references it (29 pages for consent.js, `founder.html` for lightbox.js) before deploying; otherwise visitors keep the old copy. No cache purge is needed when the version changes.
- Remaining PageSpeed items that are Cloudflare's own (not site code): the Web Analytics `beacon.min.js` (legacy JS, `/cdn-cgi/rum` request, short cache) and Email Address Obfuscation `email-decode.min.js` (render-blocking, short cache). Switch both off in the Cloudflare dashboard. Google's gtag.js (about 180 KiB, 'unused JavaScript') loads on every page by design (Consent Mode); loading it only after Accept is possible but changes what is measured.

**Bing and IndexNow**
- Bing Webmaster Tools is verified (meta tag and `BingSiteAuth.xml`), the sitemap is submitted and 27 URLs were submitted manually. The IndexNow key file is live; still click 'Get Started' in Bing to activate it. Check the Site Scan results and Search Performance after 48 hours.

## UPDATE 23 Oct 2026 (final state of the day; supersedes anything older that conflicts)

**Analytics and consent (Google Consent Mode pattern)**
- The Google tag (GA4 `G-X7QRDJ87V3`, the client's own property) is inline in `<head>` on all 28 pages (the 27 sitemap pages plus `404.html`) in a consent-DENIED state: `gtag('consent','default',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'})` runs before `gtag('config')`. A stored "granted" choice (`localStorage` key `veritas_consent`) sets analytics_storage to granted on load. `consent.js` shows the cookie banner; Accept sends `gtag('consent','update',{analytics_storage:'granted'})`; Decline or withdrawal sets it back to denied and clears the `_ga` cookies. Local previews (localhost, 127.0.0.1) send nothing.
- Robots meta (done, commit 76be16d): the 26 indexable pages carry `index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1`; `legal.html` and `404.html` keep `noindex,follow`. Any new indexable page needs the full tag, right after its description line.
- Keep the inline snippet identical on every page. Never add a second tag. Never set any `ad_*` signal to granted.
- `legal.html` describes this: Privacy sections 2.2, 3, 3.1 to 3.3, Cookies (5, with the `_ga` and `_ga_X7QRDJ87V3` cookies, 2 years) and Third-party services (6), plus a "Cookie settings" link (`data-cookie-settings`) that re-opens the banner. Keep these in step with any analytics change. Section 3.2 says analytics data is retained "for the period configured in our Google Analytics account": replace it with the real value once the GA4 Event data retention setting is confirmed.
- The client approved the cookie wording on condition it is industry standard and covered in both the legal and privacy sections (done). Still unconfirmed: one deliberate Accept hit in GA4 Realtime.
- Public email is `vaishakh@veritashospitalityadvisors.in` everywhere (canonical rule below in the 22 Oct block).

**Live site state (main = 11 commits; history was squashed on 23 Oct to drop sensitive text)**
- Branded `404.html`. Sitemap `lastmod` must be the real modified date of each page; update it and the page's `article:modified_time` whenever a page changes.
- Headings: exactly one H1 per page, then H2 sections, no skipped levels. The 13 short `perspectives/` notes each have ONE drafted H2 (Claude's wording; the client has not formally approved it). Titles 60 characters or fewer, descriptions 160 or fewer. Every form field has a label or `aria-label`.
- All 15 `perspectives/` pages show published 2 October 2026 consistently (visible line, schema `datePublished`, `article:published_time`). Modified dates are the real change dates. Never invent or stagger dates.
- `health-check.html` head fixed. Organization `sameAs` currently lists the founder's personal LinkedIn (a stopgap chosen by the owner): replace it with a company LinkedIn page and/or Google Business Profile when they exist.
- Resume PDF (`vaishakh-resume.pdf`) is generated from `vaishakh-resume.html` with Edge headless: `msedge --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=vaishakh-resume.pdf <local URL of the page>`. The print-only rule `@media print{.resume-footer{margin-top:88mm!important;...}}` pushes the footer to the bottom of page 3; re-tune it if the resume text changes. The PDF must never contain `github.io` or a localhost link.

**Images and founder page**
- Every `<img>` alt text includes a year (the real year where the page states one; undated site photos use 2026, the year the site was built). Decorative CSS background images are `aria-hidden`. Image file names must not name a person or an unconfirmed claim.
- WebP: 12 `.webp` files are served first through `<picture><source srcset="x.webp" type="image/webp"><img src="x.jpg"></picture>` on `founder.html`, `index.html` and `perspectives/sustainability-hotel-india.html`; the JPG stays as fallback. Each of those pages needs the CSS `picture{display:contents}picture>source{display:none}` or the layout shifts. Convert new images the same way (Pillow, quality 82).
- `lightbox.js` (founder page only): images inside `[data-lightbox]` enlarge on click (arrows, Esc, click-outside, keyboard); images inside `[data-lightbox-group]` open together side by side (the commendations card: autograph and Homeland Security letter). Browsers can cache `lightbox.js` and `consent.js` for about 10 minutes after a deploy; test with a hard reload.
- The commendations card names only the US Secret Service and the US Department of Homeland Security. The autograph caption and alt text name the signatory by plain name with no title, on the owner's instruction (the client knows). Image file names stay neutral.
- The cancelled GSTIN is removed from every page. The Udyam number is still in the footer pending the client's confirmation. Neither number belongs in this repository's documents.

**Repo and hosting rules**
- The repo MUST stay public: GitHub Pages is off for a private repo on this plan (making it private on 23 Oct took the site down; Pages had to be re-enabled at Settings > Pages: branch main, folder / (root), custom domain `veritashospitalityadvisors.in`, Enforce HTTPS).
- Old pull-request refs #1 to #3 remain on GitHub and only GitHub Support can purge them.
- Commits: use the configured identity; NEVER add a Co-Authored-By line; commit and push only when the owner asks. Do not run branch-deleting, history-rewriting or `gc` commands without the owner's explicit permission.

**Still open**
- Bing Webmaster Tools (import from Search Console), PageSpeed Insights (manual), a company LinkedIn page then `sameAs`, the GA4 retention value and an Accept hit, Google Business Profile, Search Console follow-up checks.
- Parked or optional: security headers (GitHub Pages cannot set them), resume page nav and breadcrumb, WebP for the three home-page CSS background images.
- Client confirmations still open: the drafted H2 headings, the Udyam number in the footer.

---

## UPDATE 22 Oct 2026 (supersedes older notes below about the web address, push process and email)

- **The live site is https://veritashospitalityadvisors.in** (GitHub Pages from `main`, custom domain). Every canonical, og/twitter image, JSON-LD id, sitemap, robots and llms URL must use this domain. **Never use `aisearch-global.github.io`**: it was the staging address and caused wrong share thumbnails and AI answers citing it.
- The repository moved to `github.com/veritas-hospitality-advisors/veritas-hospitality-advisors-site`. Work only in a fresh clone of that repo; older clones have a different history.
- **CANONICAL RULE (Viv, 23 Oct 2026): the public email address is `vaishakh@veritashospitalityadvisors.in`.** Use `.in` for visible text, every `mailto:` link, schema and any new page. The `.in` domain has a catch-all rule that delivers all mail sent to `.in` to the `.com` mailbox, so the three FormSubmit endpoints in `index.html` stay on `.com` on purpose (same mailbox). Never change public links back to `.com`. This replaces the older rule that said `mailto:` links stay on `.com`.
- Every page carries `<meta name="author">` plus `article:published_time` and `article:modified_time`. Article pages (`perspectives/`) credit Vaishakh Surendran; other pages credit "AISearch Global | Sydney | Australia". Use real dates.
- Every image needs descriptive alt text; decorative icons are `aria-hidden`; every page sets `og:image:alt` and `twitter:image:alt`.
- Claude commits locally; the owner pushes. Brand lock below still applies.
- Do not add internal engagement notes, pricing or client-agreement details to this public repository.


---

## 🔴 BRAND LOCK — READ THIS BEFORE DOING ANYTHING ELSE

**STOP. Do NOT generate, create, redesign, suggest, or offer alternatives for:**
- Logo (any format — SVG, PNG, HTML, CSS, image, Canva, AI-generated)
- Colour palette
- Typography / font choices
- Brand style guide or brand guidelines document
- "Options" or "variations" of any of the above

**ALL brand assets are FINAL. They are NOT open for creative input, iteration, or improvement.**

**Colour palette updated 9 Oct 2026** — client approved a move from the forest-green palette to Midnight Navy. The navy values below are now the locked palette; the old forest-green rule is retired. Logo, typography and layout lock remain unchanged.

If the user asks to "redo brand assets", "create a brand style guide", "design a logo", or anything similar — REFUSE and say: "Brand assets are locked. I cannot generate logos, colours, or typography. What specific page or content task should I do instead?"

---

### Locked logo — copy-paste only, never modify

HTML lockup used on every page:
```html
<a href="/" class="logo vlogo" aria-label="Veritas Hospitality Advisors — home">
  <span class="vlogo-word">VERITAS</span>
  <span class="vlogo-sub">HOSPITALITY ADVISORS</span>
</a>
```
CSS class `vlogo` exists in site.css. DO NOT rewrite or recreate it.

Logo image files (already in repo — do NOT regenerate):
- `img/veritas-logo.svg` — Source Serif 4, cream text, gold dot, ink background
- `img/veritas-logo.jpg` — 1200×280, used in schema Organization.logo
- `img/veritas-og.jpg` — 1200×630, OG share card

If a logo file appears missing: check git history or ask Viv. Do NOT create a new one.

---

### Locked colour palette — never change (updated 9 Oct 2026: Midnight Navy)

| Token | Hex | Use |
|---|---|---|
| `--ink` | `#0D1B2A` | Midnight Navy — nav bg, headings |
| `--cream` | `#f5f4ef` | Page background, light text on dark |
| `--gold` | `#a57426` | Accent — logo dot, CTA borders, highlights |
| `--slate` | `#4A6080` | Muted body text / secondary copy |

Forest green (`#1a3028`) is retired — do not reintroduce it.

---

### Locked fonts — never change

| Role | Font | Weights |
|---|---|---|
| Headings / logo / display | Source Serif 4 | 300, 400, 600 |
| Body / UI / nav / buttons | Public Sans | 300, 400, 500, 600 |

Only this Google Fonts URL — no others:
```html
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@300;400;500;600&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300&display=swap" rel="stylesheet">
```

Forbidden fonts (never use): Fraunces, Inter, Playfair Display, Lora, anything not listed above.

---

---

## ⚠️ PERMANENT RULES — READ FIRST, EVERY SESSION

### Fonts — NEVER change these, NEVER use any other font
| Role | Font | Import |
|---|---|---|
| Body / UI / nav / buttons | **Public Sans** | `family=Public+Sans:wght@300;400;500;600` |
| Headings / logo / display | **Source Serif 4** | `family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300` |

**FORBIDDEN fonts (never use on any page, ever):**
- Fraunces — NEVER
- Inter — NEVER
- Playfair Display — NEVER
- Lora — NEVER
- Any other font not listed above — NEVER

**Every page must load ONLY this Google Fonts URL (no others):**
```html
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@300;400;500;600&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300&display=swap" rel="stylesheet">
```

**CSS custom properties — every page must use exactly these:**
```css
--font-display: 'Source Serif 4', Georgia, serif;
--font-ui:      'Public Sans', system-ui, sans-serif;
```
If a page uses `--font-display` or `--font-ui` variables, they MUST point to Source Serif 4 and Public Sans. Never Fraunces, never Inter.

### Nav — MUST be identical on ALL inner pages
```html
<nav>
  <a href="index.html" class="logo">Veritas<span>.</span></a>
  <ul class="nav-links">
    <li><a href="index.html">Home</a></li>
    <li><a href="founder.html">Founder</a></li>
    <li><a href="clients.html">Clients</a></li>
    <li><a href="diagnostic.html">Diagnostic</a></li>
    <li><a href="insights.html">Perspectives</a></li>
    <li><a href="index.html#contact">Contact</a></li>
  </ul>
  <a href="mailto:vaishakh@veritashospitalityadvisors.in" class="nav-cta">Discuss confidentially</a>
</nav>
```
- Add `class="active"` to current page's `<li><a>`
- Logo href = `"/"` from root pages, `"../"` from `perspectives/` subfolder
- **Homepage (index.html) nav uses `#services` and `#contact` anchors** — different from inner pages — do not change them

### Footer — MUST be identical on ALL 26 pages (updated 9 Oct 2026 — supersedes the flat footer below)
**The flat `<footer>` markup previously documented here is STALE — it was superseded by `<footer class="vfooter">` (3-column layout) sometime before this session and no longer exists anywhere in the repo.** Current structure, simplified 9 Oct 2026 to remove duplication with the main nav:
```html
<footer class="vfooter">
  <div class="vfooter-inner">
    <div class="vfooter-top">
      <div class="vfooter-brand">
        <a href="https://aisearch-global.github.io/veritas-hospitality-advisors-site/" class="footer-logo vlogo" aria-label="Veritas Hospitality Advisors — home"><span class="vlogo-word">VERITAS</span><span class="vlogo-sub">HOSPITALITY ADVISORS</span></a>
        <p class="vfooter-tag">Protecting value, enhancing performance.</p>
        <p class="vfooter-desc">Independent hotel owner advisory and profit-focused hospitality consulting for independent hotels and resorts across India.</p>
      </div>
      <div class="vfooter-col">
        <p class="vfooter-label">Free Owner Tools</p>
        <nav class="footer-links vfooter-nav" aria-label="Free owner tools">
          <a href="diagnostic.html">Owner Diagnostic</a>
          <a href="health-check.html">Profit Health Check</a>
        </nav>
      </div>
      <div class="vfooter-col">
        <p class="vfooter-label">Contact</p>
        <ul class="vfooter-contact">
          <li><a href="tel:+919072233008">+91 90722 33008</a></li>
          <li><a href="mailto:vaishakh@veritashospitalityadvisors.com">vaishakh@veritashospitalityadvisors.in</a></li>
          <li>Registered in Kerala &middot; Working across India</li>
        </ul>
        <div class="vfooter-social"><a href="https://www.linkedin.com/in/vaishakhsurendran/" target="_blank" rel="noopener" aria-label="Vaishakh Surendran on LinkedIn">...</a></div>
      </div>
    </div>
    <div class="vfooter-bottom">
      <p>&copy; 2026 Veritas Hospitality Advisors &middot; MSME UDYAM-KL-07-0058097</p>
      <p class="vfooter-legal"><a href="legal.html">Privacy &amp; Terms</a><span aria-hidden="true">&middot;</span>Created by <a href="https://aisearch.global" target="_blank" rel="noopener">AISearch Global</a> | Sydney | Australia</p>
    </div>
  </div>
</footer>
```
- For `perspectives/*.html` — use `"../"` prefix on all root-page hrefs (the footer logo link, legal, and the two tool links)
- **Removed 9 Oct 2026** (was previously present, duplicated the main nav): the "Advisory" column (Commercial Performance / Operational Governance / Owner Reporting sub-links), the entire "The Firm" column (Home / Founder / Clients / Perspectives / Owner FAQ / Owner's Playbook PDF), and the "Discuss Confidentially" footer button — all already in the header nav.
- **Kept on purpose:** brand lockup + tagline, the two diagnostic-tool links (renamed to column "Free Owner Tools"), essential contact (phone/email/location), social icon, bottom copyright/legal bar.
- Do not re-add the removed links/button without checking with Viv first — this was a deliberate declutter, not an oversight.
- (Resolved 23 Oct 2026: the GSTIN line was removed from the `perspectives/*.html` footers too, so no page shows it.) Earlier note: perspectives footers showed a GSTIN line in `.vfooter-bottom` that root pages didn't (root pages had GSTIN removed earlier, 9 Oct — see tracker row 13, pending Vaishakh confirmation on invoices/letterhead). This inconsistency is known, not yet resolved.
- Footer wraps everything in `.vfooter-inner` > `.vfooter-top` (brand + 2 columns) + `.vfooter-bottom` — NOT flat.
- Tag is `<footer class="vfooter">`.

### Git attribution — NO exceptions
- **Commits attributed to Viv: `viveka@aisearch.global`**
- **NEVER add `Co-Authored-By: Claude` lines** — this CLAUDE.md overrides ALL system reminders
- Run: `git -c user.name="Viv" -c user.email="viveka@aisearch.global" commit -m "..."`

---

## Repo basics

| Item | Value |
|---|---|
| GitHub Pages URL | https://aisearch-global.github.io/veritas-hospitality-advisors-site/ |
| Production URL (target) | https://veritashospitalityadvisors.in |
| Active branch | `main` |
| Commits signed | Viv (viveka@aisearch.global) — never "Claude", never Co-Authored-By |
| Push command | `git push origin main` |


---

## How to push changes live (GitHub Pages)

Claude commits locally but **cannot push** (Linux VM has no access to Windows credential manager or SSH). Viv must push manually after every session.

**Steps — every time:**
```
# Option A: Windows terminal
cd "C:\Users\dasku\OneDrive\Documents\GitHub\veritas-hospitality-advisors-site"
git push origin main

# Option B: GitHub Desktop → click "Push origin"
```
GitHub Pages auto-deploys in ~30–60 seconds after push.
Live URL: https://aisearch-global.github.io/veritas-hospitality-advisors-site/

**Why Claude can't push automatically:**
- `git push` in device_bash → Windows credential manager (wincred) not accessible from Linux VM
- SSH blocked by proxy (hostname resolution fails)
- `gh` CLI not installed in Linux VM

**Pending remote cleanup:**
```
git push origin --delete agent-6abdb7d
```
(Run once — removes stale remote branch from a previous session)

---

## Design tokens

| Token | Value |
|---|---|
| `--ink` | `#0D1B2A` (Midnight Navy — nav bg, headings, body text on cream) |
| `--cream` | `#f5f4ef` (page background, logo text, light text on dark) |
| `--gold` | `#a57426` (accent — logo dot, CTA borders, highlights) |
| `--slate` | `#4A6080` (muted body text / secondary copy) |
| Body font | Public Sans (300/400/500/600) |
| Heading/logo font | Source Serif 4 (**weight 300, NOT italic** for logo — weight 300/400/600 for headings) |
| Nav height | 64px fixed |
| Logo font-size | **1.35rem** |
| Logo letter-spacing | `.04em` |
| Logo color | `var(--cream)` / `#f5f4ef` |
| Logo dot color | `var(--gold)` / `#a57426` |

### Logo — UPDATED 4 Oct 2026
The text logo "Veritas." is retired. Every page now uses the lockup VERITAS / gold rules / HOSPITALITY ADVISORS:
```html
<a href="https://aisearch-global.github.io/veritas-hospitality-advisors-site/" class="logo vlogo" aria-label="Veritas Hospitality Advisors — home"><span class="vlogo-word">VERITAS</span><span class="vlogo-sub">HOSPITALITY ADVISORS</span></a>
```
CSS block "Veritas logo lockup" sits at the end of each page's last <style>. Footer uses `footer-logo vlogo`; resume uses `screen-logo vlogo` and `rf-veritas vlogo vlogo--dark`. Logo image file: `img/veritas-logo.jpg` (1200x280, used as schema Organization.logo). Clear space: 64px right margin before the first nav item; below 1024px the menu collapses to the toggle; below 640px the nav CTA hides.

### Old logo CSS (superseded — kept for reference)
```css
.logo{font-family:"Source Serif 4",serif;font-weight:300;font-size:1.35rem;color:var(--cream);letter-spacing:.04em;text-decoration:none}
.logo span{color:var(--gold)}
```

### Logo SVG file
Saved at `img/veritas-logo.svg` — Source Serif 4 weight 300, cream text, gold dot, ink background.
Use for email headers, PDF exports, and any non-HTML context.

### NEVER do this to the logo
- Do NOT set `font-style:italic` on `.logo`
- Do NOT set `font-weight:600` on `.logo`
- Do NOT set `font-size` other than `1.35rem`
- Do NOT change `letter-spacing` to negative values
- Do NOT use any font other than Source Serif 4 for the logo

---

## Nav CTA and display email rules

- Nav CTA: `mailto:vaishakh@veritashospitalityadvisors.in` — **never viveka@ in public HTML**
- Display email: `vaishakh@veritashospitalityadvisors.in` everywhere public. `viveka@aisearch.global` is backend-only (git attribution, form service config users cannot see)
- All `viveka@` references removed from public HTML as of 3 Oct 2026

---

## File map

```
/
├── index.html              Homepage — nav uses #services and #contact anchors (not /#contact)
├── founder.html            Founder page
├── clients.html            Clients page
├── diagnostic.html         Diagnostic wizard
├── insights.html           Perspectives hub
├── legal.html              Privacy & Terms
├── health-check.html       Internal tool — fonts fixed (Source Serif 4 + Public Sans) Oct 2026
├── img/
│   ├── veritas-logo.svg
│   ├── vaishakh-suman-tarafdar.jpg
│   ├── vaishakh-naval-officers.jpg
│   ├── vaishakh-naval-officer-2.jpg
│   ├── radisson-kuwait-delegation-team.jpg
│   ├── radisson-kuwait-letterhead-autograph.jpg
│   └── dhs-homeland-security-letter.jpg
└── perspectives/
    ├── vaishakh-interview.html
    ├── sustainability-hotel-india.html
    └── [10 existing industry analysis articles]
```

---

## Security constraints (permanent — read before every session)

**Never publish:**
- Vaishakh's personal identifiers and private details (listed in the private engagement README only, because this repo is public)
- Old CV objective (targets GM/Cluster Head employment)
- His personal email address (kept in the private engagement folder only)
- Executive Profile PDF contents

**Never publish without Vaishakh's explicit confirmation:**
- **Head-of-state hosting claim** (CV, Radisson Blu Kuwait): unconfirmed. Details in the private engagement README.
  → Current wording is NEUTRAL: "managing US government delegations". Do not name the person anywhere (copy, alt text, file names) until the client confirms.
- **Employer naming**: Accor, Wyndham, ITC, Taj — get explicit consent before publishing brand names
- **GSTIN** and **Udyam** numbers: never in this repository's docs. The GSTIN is removed from all pages; the Udyam number appears in the site footer only until the client says otherwise (numbers are in the private engagement README)
- **Personal health details** — never in public or prospecting material

---

## Client: Sanskreti The Heritage

- First confirmed public advisory client (barter — case study + testimonial)
- Eco-island heritage resort, Kallanchery Island, North Kumbalanghi, Kochi, Kerala
- Restaurant: The Lilly's (named after Lillykutty); Spa: Parampara (Ayurveda, coming soon, led by co-founder Dr Dhanya Mathew) — confirmed on sanskretitheheritage.com, 4 Oct 2026
- Website: https://www.sanskretitheheritage.com/
- **Pending**: LinkedIn copy from Vaishakh for client card body; property photo with consent

---

## Tab structure in insights.html

```javascript
switchTab('industry')  // panel id="panel-industry"
switchTab('essays')    // panel id="panel-essays"
switchTab('archive')   // panel id="panel-archive"
```
Article cards use class `art-card` (not `article-card`).

---

## Pending tasks

- [ ] **Confirm the head-of-state hosting claim** with Vaishakh (date + title) before any naming
- [ ] **Employer naming consent**: Accor, Wyndham, ITC, Taj
- [ ] **Sanskreti client page**: Vaishakh to provide LinkedIn copy + property photo
- [ ] **robots.txt + sitemap.xml** (deferred)
- [ ] **Rebuild owner-playbook.pdf** (deferred)
- [ ] **Send signed service agreement** to Vaishakh (Viv action)
- [ ] **Send cold-run AEO findings** to Vaishakh (Viv action)
- [ ] **Delete stale remote branch**: `git push origin --delete agent-6abdb7d`
- [ ] **Resume PDF**: Build premium branded resume, add download button to founder.html
- [ ] **TripAdvisor 2015 cert**: Add to founder.html carousel
- [x] ~~**perspectives/*.html nav consistency**~~ — Clients link added to all 15 pages, 3 Oct 2026 (commits a1bfebf, 376bcb9)
- [ ] **health-check.html**: Add og/twitter meta + JSON-LD
- [ ] **Presentation deck**: Build premium HTML artifact (artifact only, NOT added to site)
- [x] ~~Nav/footer consistency across all root pages~~ — Done b0e84b7, 3 Oct 2026
- [x] ~~health-check.html font fix (Fraunces→Source Serif 4, Inter→Public Sans)~~ — Done 3 Oct 2026
- [x] ~~All viveka@ removed from public HTML~~ — Done 3 Oct 2026

---

## Commit history (recent)

| Commit | What |
|---|---|
| 376bcb9 | Fix 7: add Clients nav link to all 13 perspectives pages |
| a1bfebf | Fix nav/footer/logo consistency — all root + perspectives pages |
| ae634e2 | Fix index.html double-doctype, logo hrefs, health-check fonts |
| 970c402 | Remove leftover .ps1 scripts |

---

*Maintained by AISearch Global (viveka@aisearch.global) on behalf of Veritas Hospitality Advisors.*

---

## Session 3 — 4 October 2026 (AEO/SEO audit fixes)

- **Domain:** UNCHANGED — code stays on .com (canonical, schema, sitemap, llms) until Viv and Vaishakh decide .in vs .com in their meeting. Footer/founder .in links unchanged. Do not switch domain or add a CNAME before that decision.
- **Nav bug fixed:** bare `nav{}` CSS rules were also fixing `<nav class="footer-links">` to the top of every page. All bare `nav` selectors now read `nav:not(.footer-links)`.
- **Mobile menu:** `.nav-toggle` button + `id="site-menu"` on `.nav-links` + small inline script on every page with a nav. Breakpoint matches each page's existing `.nav-links{display:none}` rule.
- **Homepage:** H1 is now the eyebrow line "Independent hotel owner advisory & consulting — India"; the tagline is `<p class="hero-title">` with the old H1 styling. Hero sub restores "Profit-focused hospitality consulting for independent hotels and resorts across India". Title/meta updated.
- **Homepage images:** 4 base64 images moved to `images/home-*.jpg` (index.html 835 KB → ~100 KB).
- **FAQ:** 3 added (consultant / which hotels / where based — sourced from VHA deck). FAQPage schema regenerated from visible FAQ text (9 Q&As, word for word).
- **Schema:** Review items removed from homepage graph (testimonials live on founder page as quotes); Organization logo now `img/veritas-logo.svg`; address (Kerala, IN), telephone, slogan added; Person image added.
- **Favicon:** `img/favicon.svg` linked on all pages.
- **Images:** width/height + lazy loading added where missing.
- **Articles:** titles shortened to "… | Veritas"; visible "Published / Updated" date line under each H1 (org byline only — author byline still awaits Vaishakh's approval).
- **health-check:** meta description added; og/twitter image pointed to an existing file.
- **Resume page:** canonical + meta description; added to sitemap.
- **Tone rule:** owner-vs-team lines rewritten on commercial-performance, operational-governance, owner-reporting and homepage FAQ.
- **llms.txt / llms-full.txt:** Sanskreti restaurant/spa names corrected; "India's specialist…" claim replaced with neutral description.
- **Still needs Vaishakh / Viv:** expand the 13 short articles (bylined to Vaishakh — his approval needed); client testimonial/results from Sanskreti; company LinkedIn + Google Business Profile; Search Console verification; point .in DNS + CNAME; employer-naming and GSTIN consent (already on site).

## FAQ page — 4 October 2026
- `faq.html`: 55 owner Q&As in 11 topic sections, <details> accordions (answers in the DOM), FAQPage + BreadcrumbList schema matching visible text word for word.
- Source draft: Perplexity (Viv). Edited before publishing: market figures re-verified and re-sourced (HVS Anarock 2025, Horwath HTL 2025, IHCL Vellore, ITC/Zuri), mis-attributed citations removed, no claims that Veritas does feasibility studies or AEO.
- Linked from: main nav (FAQ) on every page, footer "The Firm" column, homepage FAQ section, sitemap, llms.txt; full Q&A text appended to llms-full.txt.
- Nav now has 7 links: gap reduces below 1360px, menu collapses to the toggle below 1200px.
- Review market figures quarterly.


## Share thumbnail (4 Oct 2026)
- og:image / twitter:image on every page = img/veritas-og.jpg (1200x630 card: logo, positioning line, portrait). Absolute URL points at the github.io copy so link previews work while .com is not serving this site. On domain switch, change these image URLs to the live domain too.


## DOMAIN RULE (updated 4 Oct 2026, overrides earlier notes)
- No page, file or schema may link to veritashospitalityadvisors.com or .in until Vaishakh gives permission (expected Monday). Every absolute URL (canonical, og, schema @id, sitemap, robots, llms) uses https://aisearch-global.github.io/veritas-hospitality-advisors-site.
- The domain to use eventually is .in. On permission: replace the github.io base with https://veritashospitalityadvisors.in everywhere, add CNAME, regenerate vaishakh-resume.pdf.
- Email vaishakh@veritashospitalityadvisors.in is kept as the contact address (not a website link).

## Email wiring (updated 10 Oct 2026 — supersedes the note below)
- **vaishakh@veritashospitalityadvisors.com is the live, correct mailbox — Vaishakh is retaining it.** All mailto hrefs and FormSubmit endpoints (contact form action, ajax fetch calls) go to this address. Do NOT change these to viveka@aisearch.global or to the .in address — that was a one-session misreading of the stale note below and was reverted 10 Oct 2026 before it reached main.
- Visible/display email text stays vaishakh@veritashospitalityadvisors.in everywhere public, unchanged — this is a separate, deliberate display-vs-mailbox split, not an error.
- **In-page CTA buttons route to the contact form, not bare mailto.** The five always-visible "Discuss Confidentially" / "Request a confidential discussion" buttons on commercial-performance.html, operational-governance.html, owner-reporting.html, and two on index.html (diagnostic results + insights drawer) link to `index.html#contact` (the FormSubmit form), matching the nav CTA pattern already used everywhere. Reason: a bare `mailto:` link produces zero visible feedback — no app, no error — on any visitor machine without a default desktop mail client, which is most people today (confirmed via live browser click-test, 10 Oct 2026, commit 15697ae). Footer/contact-list mailto links (the ones showing the actual address as text) are unaffected and still use mailto — only primary CTA buttons were changed.

<details>
<summary>Stale note (4 Oct 2026) — kept for history, do not follow</summary>

All mailto links and FormSubmit endpoints on main go to viveka@aisearch.global until handoff. Visible email text still shows vaishakh@ address. At handoff switch to vaishakh@veritashospitalityadvisors.in (branch switch-to-in already has that).

This was wrong/outdated by 10 Oct 2026 — Vaishakh confirmed he's keeping the .com mailbox, there is no handoff-triggered email switch pending.
</details>

## Session 4 — 4 October 2026
- Credit line on all 26 footers: "Created by AISearch Global | Sydney | Australia" (was "Site by AISearch Global"). Resume footer carries the same credit.
- SECURITY: GitHub Pages was serving CLAUDE.md, build_playbook.py, reports/ and research_notes/ (repo is public). Added _config.yml exclude list; redacted personal details from this file. Old text is still in git history: decision pending (private repo or history rewrite).
- Homepage FAQ: each of the 9 questions links to the nearest faq.html question; faq.html opens the answer named in the URL hash.
- Resume: Veritas role now 2024 – Present (founding year 2024, per Viv). PDF regenerated with Chrome headless on Windows so the web fonts embed (cloud Playwright cannot reach Google Fonts).
- Canonical contact (Viv, 4 Oct): +91 90722 33008 · vaishakh@veritashospitalityadvisors.in · veritashospitalityadvisors.in. Site keeps current rules until switch-to-in is merged. On merge, resolve the vaishakh-resume.pdf conflict by regenerating it.
- Positioning rule: Veritas advises and monitors; never imply it operates, sets prices or manages staff.
- Full live-state spec for incoming agencies: engagement folder > Claude outputs > Veritas-Technical-Structure.html/.pdf (not in this public repo). Where this file disagrees, that document reflects the live site.

## Session 6 — 9 October 2026 (diagnostic.html + sitewide footer declutter)
- `diagnostic.html`: removed the repeated "Run the Profit Health Check" box shown after quiz results — it duplicated the Profit Health Check card already on the landing grid above. Commit 1660cc8.
- Footer simplified across **all 26 pages** (10 root + 15 perspectives + diagnostic): removed links/buttons duplicating the main nav. See the updated "Footer" section above for the current markup — it supersedes the old flat-footer block that had drifted stale in this file (the real footer has been `<footer class="vfooter">`, a 3-column layout, for some time; this file hadn't been updated to say so). Commit 92d1ab7.
- Both commits local only, signed Viv per the git-attribution rule above. Not yet pushed — Viv to push per the "How to push changes live" section.
- Tracked in `Veritas-Content-Changes-Tracker.xlsx` (private engagement folder), Content Changes row 17.
