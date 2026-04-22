# bypass-flag-secure-android

This repository documents how `FLAG_SECURE` works in Android apps and explains patching approaches used in reverse-engineering practice.

## Important

Use this material only for:

- Personal research
- Security learning
- Testing apps you own or are authorized to assess

Do not use this to violate app policies, privacy, or local laws.

## What is covered

- Where `FLAG_SECURE` appears in Smali
- Typical patch points (`setFlags`, `addFlags`)
- Manual and regex-assisted patch workflows

## References

- Android `WindowManager.LayoutParams.FLAG_SECURE`
- Android `Display.FLAG_SECURE`
