# QibCode — company website

Static website for QibCode, an independent software studio in South Korea. The first product is **Korean Naturalization Interview Practice** for Android.

The site uses plain HTML, CSS and JavaScript. There is no build step.

## Important release alignment

The public copy is now aligned with the current Android product architecture:

- chapter-based protected video practice rather than multiple-choice mock tests;
- Practice Needed / Practice Done / Deleted tracking;
- Continue Practice, Update Practice Chapters and Start From Scratch;
- 15-minute online-verified trial;
- planned ₩19,900 one-time full unlock for Chapters 1–6 + Supplementary;
- full-access offline use after content download/verification;
- Firebase-backed authentication/access, device registration, entitlement and trial usage;
- local practice progress and metadata caches;
- Android / Google Play at launch (no iOS claim).

Before launch, verify the final price, exact authentication flow, purchase implementation, offline-verification period and privacy disclosures against the production build.

## Structure

```
.
├── index.html
├── apps/korea-naturalization-practice/index.html
├── support/index.html
├── privacy/index.html
├── data-deletion/index.html
├── terms/index.html
├── 404.html
├── assets/css/style.css
├── assets/js/main.js
├── assets/img/
├── site.webmanifest
├── robots.txt
├── sitemap.xml
└── .nojekyll
```

## Deploy to GitHub Pages

1. Create a GitHub repository.
2. Push the contents of this folder.
3. In **Settings → Pages**, choose **Deploy from a branch**, `main`, `/ (root)`.
4. Add your custom domain after you own it and update DNS according to GitHub's current documentation.
5. Enable HTTPS after DNS verification succeeds.

## Before publishing

- Confirm that `qibcode.com` and `hello@qibcode.com` are actually controlled by you. If not, replace them everywhere before publishing.
- Replace the placeholder app icon if needed.
- Add the final Google Play URL to the app page when the listing exists.
- Link the privacy policy from inside the Android app as well as from Play Console.
- If the app offers user-facing account creation, ensure the production app also has an in-app account-deletion path and use `/data-deletion/` as the external deletion resource where appropriate.
- Have the privacy policy and terms reviewed for your final production behavior and local legal requirements.

## Local test

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.
