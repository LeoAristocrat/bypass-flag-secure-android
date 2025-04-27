# 🚫 Bypass Android FLAG_SECURE Restrictions
> Disable screenshot and screen recording restrictions on Android apps by bypassing `FLAG_SECURE`.

---

## 📜 Overview

Many Android apps prevent screenshots and screen recordings by setting a flag called `FLAG_SECURE`.  
This flag has a constant value of `8192 (0x00002000)`.

This guide explains how to **bypass FLAG_SECURE** by editing Smali code manually or using regex automation in tools like MT Manager.

---

## 📚 Official Documentation

- [WindowManager.LayoutParams.FLAG_SECURE](https://developer.android.com/reference/android/view/WindowManager.LayoutParams#FLAG_SECURE)
- [Display.FLAG_SECURE](https://developer.android.com/reference/android/view/Display#FLAG_SECURE)

---

## 🔥 How FLAG_SECURE Is Used

In Android apps, you will usually find code like:
```smali
Landroid/app/Activity;->getWindow()Landroid/view/Window;
```
Then followed by methods:
```smali
Landroid/view/Window;->setFlags(II)V
Landroid/view/Window;->addFlags(I)V
```
If you see the `0x2000` constant being used in these functions, it is responsible for enabling screenshot and recording restrictions.

---

## 🛠 Manual Bypass

### Steps:
1. Open the decompiled Smali code.
2. Search for calls to `addFlags` or `setFlags`.
3. Check if the constant `0x2000` is used.
4. Replace `0x2000` with `0x0`.

This change disables the secure flag, allowing screenshots and recordings.

---

## 🧩 Automated Bypass using Regex (MT Manager)

To speed things up, you can automate the search and replace process with a regex.

### Regex to Search
```regex
(const\/)16(\s[pv]\d{1,2},\s0x)200(0\n\n(\s{4}\.line\s\d+\n)?\s{4}invoke-virtual\s\{[pv]\d{1,2},\s[pv]\d{1,2}(,\s[pv]\d{1,2})?\},\sLandroid\/view\/Window;->(add|set)Flags\(II?\)V)
```

### Replacement Text
```text
$14$2$3
```

✅ **Explanation:**
- `$14` is **the digit 4** added after the first captured group (it is not referring to a capture group number).
- It modifies the flag value from `0x2000` to `0x0`.

---

## 🛠 Recommended Tools

| Tool | Purpose |
|:----:|:--------|
| [MT Manager](https://mt2.cn/) | APK editor for Android |
| [Jadx](https://github.com/skylot/jadx) | Decompiler to Java source |
| [Smali/Baksmali](https://github.com/JesusFreke/smali) | Smali disassembler/assembler |

---

## ⚠️ Important Notes

- This regex works in **most simple cases** but **not 100% universal**.
- Complex apps may hide the secure flag dynamically or obfuscate the value.
- Manual analysis is needed for highly protected apps.
- Always create a **backup** of the APK before making changes.

---

## 📢 Legal Disclaimer

This guide is for **educational purposes only**.  
Modifying APK files may **violate terms of service** or **local laws**.  
The author assumes **no responsibility** for any misuse.

---

## ⭐ Support

If you find this project useful, please consider giving it a ⭐ to support further development!

---

# Thank you for reading! 🚀

