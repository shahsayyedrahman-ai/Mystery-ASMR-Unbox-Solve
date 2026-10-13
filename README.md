# Mystery ASMR: Unbox & Solve — PWA Packaging & Microsoft Store Guide
This directory contains the production-ready Progressive Web App (PWA) release candidate for **Mystery ASMR: Unbox & Solve** (V1.0), prepared for Windows packaging via [PWABuilder](https://www.pwabuilder.com) and distribution on the Microsoft Store.
---
## Directory Structure
```text
mystery_asmr_pwa_release/
├── index.html                 # Self-contained game client with PWA manifest & SW hooks
├── manifest.webmanifest       # W3C Web App Manifest with Windows tile & store declarations
├── service-worker.js          # Cache-First offline caching and lifecycle manager
├── icons/                     # Complete app icon set (44x44, 71x71, 150x150, 192x192, 310x310, 512x512, SVG)
│   ├── icon-44.png            # Windows App list / Small tile
│   ├── icon-71.png            # Windows Small tile
│   ├── icon-150.png           # Windows Medium tile
│   ├── icon-192.png           # Standard PWA icon
│   ├── icon-310.png           # Windows Large tile
│   ├── icon-512.png           # High-resolution store asset
│   ├── icon-maskable-192.png  # Adaptive maskable icon
│   ├── icon-maskable-512.png  # High-res adaptive maskable icon
│   ├── icon-32.png            # Favicon
│   └── icon.svg               # Scalable vector master
├── validate_pwa.py            # Automated PWA verification & offline relaunch test runner
├── v10_validation.py          # V1.0 25-check dedicated validation suite
├── v09_validation.py          # V0.9 9-check dedicated validation suite
├── RELEASE_MANIFEST.md        # Cryptographic SHA-256 checksums of all release files
└── README.md                  # This document
```
---
## Stage 1: Hosting over HTTPS
PWABuilder and the Microsoft Store require the PWA to be hosted on an active HTTPS domain.
### Recommended Free / Static Hosts
1. **GitHub Pages**:
   - Push this directory to a GitHub repository branch.
   - Enable GitHub Pages in repository settings.
   - Your URL will be `https://<username>.github.io/<repo-name>/`.
2. **Cloudflare Pages / Netlify / Vercel**:
   - Connect the repository or drag-and-drop this folder.
   - Immediate automatic HTTPS with HTTP/2 and global CDN caching.
3. **Azure Static Web Apps / Firebase Hosting**:
   - Run `firebase deploy` or deploy via Azure CLI.
### Hosting Requirements Checklist
- [x] Served strictly over **HTTPS** (or `localhost` for local debugging).
- [x] MIME type for `manifest.webmanifest`: `application/manifest+json` (or `application/json`).
