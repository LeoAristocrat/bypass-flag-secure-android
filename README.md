<p align="center">
  <img src="https://raw.githubusercontent.com/LeoAristocrat/bypass-flag-secure-android/main/banner.png" alt="Bypass FLAG_SECURE Banner" width="800">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android-green?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/Method-Smali%20Patch-blue?style=for-the-badge" alt="Method">
  <img src="https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Status-Stable-success?style=for-the-badge" alt="Status">
</p>

# 🚀 Bypass FLAG_SECURE in Android Apps

> Smali Regex Patch + Frida Script to allow screenshots and screen recording in apps that normally block it.

---

## 📚 Overview

Many Android apps (like banking apps, OTT apps, and security-sensitive apps) set a flag called `FLAG_SECURE` to prevent taking screenshots or screen recording.

This project provides **two simple methods** to bypass `FLAG_SECURE`:

- **Method 1:** Modify Smali code using a Regex Patch (using MT Manager)
- **Method 2:** Use a Frida Hook Script during app runtime

---

## 📦 Project Structure

| Folder / File | Description |
|:-------------|:------------|
| `regex/mt_manager_regex.txt` | Regex search and replace pattern for MT Manager |
| `scripts/frida_bypass_flag_secure.js` | Frida script to bypass FLAG_SECURE |
| `LICENSE` | MIT License |
| `.gitignore` | Ignore temporary and build files |
| `README.md` | Complete documentation |
| `banner.png` | Repository banner image |

---

## 🛠️ Usage Instructions

### 🔹 Method 1: MT Manager Smali Patch (Recommended)

1. Open the APK in **MT Manager** (or any APK editor that supports Smali editing).
2. Search for the following **Regex** in Smali files:
