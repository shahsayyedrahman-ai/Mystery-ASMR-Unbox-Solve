import os
import hashlib
import json

RELEASE_DIR = r'C:\Users\mkbaghel\.gemini\antigravity\scratch\mystery_asmr_pwa_release'

FILE_DESCRIPTIONS = {
    'index.html': 'Self-contained single-file HTML5 playable game with PWA manifest link and service-worker registration.',
    'manifest.webmanifest': 'W3C Web App Manifest containing app identity, display mode, theme colors, icons, and shortcuts.',
    'service-worker.js': 'Offline caching service worker using Cache-First / Stale-While-Revalidate strategy with safe lifecycle management.',
    'validate_pwa.py': 'Automated PWA verification script testing manifest, service worker, cache storage, and offline relaunch via CDP.',
    'v10_validation.py': 'V1.0 dedicated validation test suite (25 test assertions covering quests, economy, and state).',
    'v09_validation.py': 'V0.9 dedicated validation test suite (9 test assertions covering item star mastery).',
    'icons/icon-44.png': '44x44 App list / Small tile icon for Windows and taskbar display.',
    'icons/icon-71.png': '71x71 Small tile icon for Windows Start menu.',
    'icons/icon-150.png': '150x150 Medium tile icon for Windows Start menu.',
    'icons/icon-192.png': '192x192 Standard PWA home screen icon.',
    'icons/icon-310.png': '310x310 Large tile icon for Windows Start menu.',
    'icons/icon-512.png': '512x512 High-resolution PWA splash / Microsoft Store asset.',
    'icons/icon-maskable-192.png': '192x192 Adaptive maskable PWA icon with safe-zone margin.',
    'icons/icon-maskable-512.png': '512x512 High-res adaptive maskable PWA icon with safe-zone margin.',
    'icons/icon-32.png': '32x32 Favicon icon for browser tab display.',
    'icons/icon.svg': 'Scalable vector icon in SVG format.',
    'README.md': 'Hosting, packaging, and Microsoft Partner Center PWABuilder workflow instructions.',
    'RELEASE_MANIFEST.md': 'Cryptographic SHA-256 release manifest of all packaged PWA assets.'
}

def generate_manifest():
    entries = []
    for root, dirs, files in os.walk(RELEASE_DIR):
        for f in sorted(files):
            if f in ('generate_manifest.py', 'RELEASE_MANIFEST.md'):
                continue
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, RELEASE_DIR).replace('\\', '/')
            with open(path, 'rb') as fp:
                content = fp.read()
                digest = hashlib.sha256(content).hexdigest()
                size = len(content)
            desc = FILE_DESCRIPTIONS.get(rel_path, 'Packaged release file')
            entries.append({
                'file': rel_path,
                'size': size,
                'hash': digest,
                'description': desc
            })

    output_lines = [
        "# MYSTERY ASMR: UNBOX & SOLVE — RELEASE MANIFEST",
        "",
        "**Release Candidate**: V1.0  ",
        f"**Directory**: `{RELEASE_DIR}`  ",
        "**Packaging Standard**: Microsoft Store PWA (W3C Web App Manifest + Service Worker)  ",
        "",
        "## File Verification & SHA-256 Hashes",
        "",
        "| File | Size (Bytes) | SHA-256 Checksum | Purpose / Description |",
        "| :--- | :---: | :--- | :--- |"
    ]

    for e in entries:
        output_lines.append(f"| `{e['file']}` | {e['size']} | `{e['hash']}` | {e['description']} |")

    output_lines.extend([
        "",
        "---",
        "",
        "## Integrity Verification Command",
        "",
        "To verify all files against this manifest on Windows PowerShell:",
        "",
        "```powershell",
        "Get-ChildItem -Recurse -File | ForEach-Object {",
        "    [PSCustomObject]@{",
        "        Name = $_.FullName.Replace((Get-Location).Path + '\\', '')",
        "        SHA256 = (Get-FileHash -Path $_.FullName -Algorithm SHA256).Hash",
        "    }",
        "} | Format-Table -AutoSize",
        "```"
    ])

    manifest_path = os.path.join(RELEASE_DIR, 'RELEASE_MANIFEST.md')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines) + '\n')

    print(f"RELEASE_MANIFEST.md generated successfully with {len(entries)} file entries.")

if __name__ == '__main__':
    generate_manifest()
