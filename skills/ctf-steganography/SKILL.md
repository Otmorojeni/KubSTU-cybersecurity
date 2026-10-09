---
name: ctf-steganography
description: >-
  Expert CTF steganography and file format analyst for extracting hidden data from
  images (PNG, JPG, BMP, GIF), audio files (WAV, MP3), archives, and documents.
  Masters tools like zsteg, steghide, exiftool, binwalk, Sonic Visualiser, and PNG chunk repair.
---

# CTF Steganography & Hidden Data Analysis

This skill provides checklists, methodologies, and CLI tool workflows for solving CTF steganography challenges.

## 1. Fast Initial Triage (File Analysis)

When given a media file (`file.png`, `audio.wav`, `doc.pdf`, `mystery.bin`):

1. **Verify Real File Type:**
   ```bash
   file challenge_file
   xxd challenge_file | head -n 5
   ```
2. **Metadata & Strings Inspection:**
   ```bash
   exiftool challenge_file
   strings -a -n 7 challenge_file | grep -Ei "flag|ctf|{|key|pass"
   ```
3. **Embedded Files & Polyglots:**
   ```bash
   binwalk -e challenge_file
   foremost -i challenge_file -o output_dir/
   ```

---

## 2. Image Steganography

### PNG / BMP (Lossless Formats)
- **zsteg:** Indispensable for PNG and BMP LSB inspection:
  ```bash
  zsteg -a image.png
  zsteg -E "b1,rgb,lsb,xy" image.png > extracted.bin
  ```
- **StegSolve:**
  - View individual bit planes (Red 0, Green 0, Blue 0, Alpha).
  - Check Stereogram solver, Frame browser (for animated GIFs or multi-layer PNGs).
- **Corrupted Dimensions / CRC Errors:**
  - If PNG looks cropped or doesn't open:
    ```bash
    pngcheck -v image.png
    ```
  - Often the height in the `IHDR` chunk is artificially lowered to hide data below the viewport. Fix height in hex editor or calculate correct height using CRC32 brute-force.
- **Color Palette & PLTE:**
  - Look for hidden ASCII or non-standard color indices in indexed-color PNGs.

### JPG / JPEG (Lossy Formats)
- **steghide:**
  ```bash
  steghide extract -sf image.jpg -p ""
  stegseek image.jpg /usr/share/wordlists/rockyou.txt
  ```
- **OutGuess / JPHide / F5:**
  ```bash
  outguess -r image.jpg output.txt
  ```

---

## 3. Audio Steganography (WAV / MP3)

- **Spectrogram View:**
  - Open in **Sonic Visualiser** or **Audacity**.
  - Switch waveform display to **Spectrogram** (look for text, QR codes, or visual keys drawn in high frequencies).
- **Morse Code & DTMF Tones:**
  - High/low beeps $\rightarrow$ Morse code decoder.
  - Phone keypad tones $\rightarrow$ DTMF decoder (`multimon-ng` or online DTMF decoders).
- **LSB in Audio:**
  - `wavsteg` or custom Python scripts reading 16-bit PCM samples.

---

## 4. Archive & Document Stegano

- **ZIP Tricks:**
  - Data appended after end-of-central-directory record (`PK\x05\x06`).
  - Encrypted zip: try `fcrackzip -u -D -p rockyou.txt file.zip` or `zip2john file.zip > hash.txt && john hash.txt`.
- **PDF & Office Documents:**
  - `pdfdetach -list document.pdf`
  - Unzip `.docx` / `.xlsx` (they are ZIP archives): inspect `word/media/`, `customXml/`, and document properties.
