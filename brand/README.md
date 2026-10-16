# The Switch — brand files (16 Oct 2026)

Every file here is either a byte-for-byte copy of a file the apps / site ship, or a
transparent PNG rasterisation of an official SVG (rendered in Chromium at an exact
multiple of its viewBox — no edits to shapes, colours or spacing). Nothing was redrawn
or composed. Sources are in the web repo `ondemandtd/fiftyfree` (local clone
`~/Code/fiftyfree-7404b414`).

| File | Pixels | What it is | Source (path @ commit) | Identical or rasterised |
|---|---|---|---|---|
| `switch-xx-mark-gold-1075x1150.png` | 1075×1150, transparent | XX chromosome mark, gold (#C79A52, #4A3413 bands) | `public/brand/switch/switch-xx-chromosome-mark.svg` @ e7a5f0aa | Rasterisation of that SVG at 2.5× |
| `switch-xx-mark-ivory-1075x1150.png` | 1075×1150, transparent | XX mark, ivory (#F8F3ED, #8A7A63 bands) — the colourway in the extension card header and the apps (same shapes as `ios/…/SwitchMark.imageset/switch-mark.svg` and `android/…/drawable/switch_mark.xml`) | `public/brand/switch/switch-xx-chromosome-mark-ivory.svg` @ e7a5f0aa | Rasterisation of that SVG at 2.5× |
| `the-switch-lockup-horizontal-on-dark-2326x384.png` | 2326×384, transparent | Horizontal lockup "XX \| THE SWITCH": gold mark, divider, ivory wordmark (text is outlined paths in the SVG) | `public/brand/switch/the-switch-lockup-horizontal-on-dark.svg` @ a0fd9742 | Rasterisation of that SVG at 8× |
| `app-icon-ios-1024.png` | 1024×1024, opaque (App Store icons carry no alpha) | The app icon: lit-gold mark with glow on the plum gradient | `ios/TheSwitch/Assets.xcassets/AppIcon.appiconset/icon-1024.png` @ ac2df6df (current on origin/ios-card-close 778a7195) | Byte-identical |
| `android-launcher-foreground-xxxhdpi-432.png` | 432×432, transparent | The launcher icon's foreground layer: the lit-gold glowing mark alone | `android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_foreground.png` @ ac2df6df (current on origin/android-card-close c2816323) | Byte-identical (largest size shipped) |
| `switch-xx-chromosome-mark.svg` | vector | Gold mark source | `public/brand/switch/switch-xx-chromosome-mark.svg` @ e7a5f0aa | Byte-identical |
| `switch-xx-chromosome-mark-ivory.svg` | vector | Ivory mark source | `public/brand/switch/switch-xx-chromosome-mark-ivory.svg` @ e7a5f0aa | Byte-identical |
| `the-switch-lockup-horizontal-on-dark.svg` | vector | Lockup source | `public/brand/switch/the-switch-lockup-horizontal-on-dark.svg` @ a0fd9742 | Byte-identical |

## What does not exist as an official file

- **A "pink-into-gold" mark.** No shipped file has the mark in a pink-to-gold
  treatment. The mark ships flat gold or flat ivory. The only pink/plum is the app
  icon's *background* gradient, behind a lit-gold mark. The closest files are
  `app-icon-ios-1024.png` (the whole icon) and
  `android-launcher-foreground-xxxhdpi-432.png` (the glowing gold mark on
  transparent — only 432 px; there is no larger transparent copy).
- **The extension card header's lockup as one file.** The card header is put
  together at runtime in `extension/content.js`: the inline ivory mark SVG
  (`MARK_SVG`) plus the live CSS text "The Switch". There is no image of it. The
  official horizontal lockup (gold mark + ivory text) is the file above.
