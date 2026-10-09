---
name: ctf-osint
description: >-
  Expert CTF open-source intelligence (OSINT) investigator for discovering flags
  and answers through geolocation, reverse image search, digital footprints,
  social media accounts, username enumeration, metadata, and web archive research.
---

# CTF OSINT (Open Source Intelligence) Investigation

This skill provides methodologies, pivots, and tooling for solving CTF OSINT challenges.

## 1. Core Principles of CTF OSINT

- **Challenge Authors Leave Breadcrumbs:** Unlike real-world hunting, CTF OSINT always has a deliberate, uniquely identifiable path leading to the flag or specific question answer.
- **Pivot Mentality:** Start with a single clue (photo, handle, email, domain, phone snippet) and pivot to find connected identities, repositories, commits, or archives.
- **Verify Specificity:** Confirm matches using multiple data points (e.g., matching username + bio phrase + creation date) to avoid rabbit holes.

---

## 2. Image & Geolocation OSINT

1. **Reverse Image Search Engines:**
   - Always test multiple engines: Google Lens, Yandex Images (often best for Russian/CIS locations and faces), Bing Visual Search, TinEye, Baidu.
2. **Metadata & Exif:**
   - Look for GPS coordinates, camera model, date taken:
     ```bash
     exiftool photo.jpg | grep -iE "gps|date|model|make"
     ```
3. **Visual Clues for Geolocation:**
   - Architecture, signs, road markings, car license plates, shop signs.
   - Street furniture: lamp post designs, power outlets, trash bins, utility poles.
   - Public transport: bus route numbers, train station emblems.
   - Flora and landscape: mountains in background, tree types, climate.
   - Sun / Shadow analysis: use SunCalc (suncalc.org) or ShadowMap to verify time of day and cardinal directions.
4. **Mapping & Verification:**
   - Google Maps & Street View / Yandex Maps & Panoramas.
   - Overpass Turbo (OpenStreetMap query tool) for combinations like `amenity=cafe` near `railway=station`.

---

## 3. Nickname, Account & Email Pivoting

1. **Username Enumeration:**
   - Tools: `whatsmyname.app`, `sherlock`, `maigret`.
   - Check developer platforms: GitHub, GitLab, Docker Hub, PyPI, NPM, Keybase.
2. **GitHub Forensics:**
   - Inspect commit logs and email addresses:
     ```bash
     git log --pretty=format:"%an <%ae>"
     ```
   - Check hidden branches, forks, deleted commits, and `.patch` / `.diff` URLs: `https://github.com/user/repo/commit/<hash>.patch`.
   - Inspect `https://api.github.com/users/<username>/events/public`.
3. **Email Pivots:**
   - HaveIBeenPwned, Epieos (Google account discovery), Hunter.io.

---

## 4. Web History & Infrastructure OSINT

1. **Archives & Caches:**
   - Wayback Machine (`archive.org/web/`).
   - Archive.today / Archive.is.
   - Google Cache / Bing Cache.
2. **Domain & DNS Footprinting:**
   - Certificate Transparency logs: `https://crt.sh/?q=%.domain.com`.
   - WHOIS historical records.
   - ViewDNS.info, SecurityTrails, Shodan / Censys for open ports and banners.
