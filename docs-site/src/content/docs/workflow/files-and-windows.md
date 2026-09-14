---
title: Files and windows
description: Open, save, and grant folders through the iOS Files app.
---

## App storage

Blender can read and write its app container normally. Enable **On My iPhone**
or **On My iPad** in Files to browse local documents. Keep a second copy of
important projects outside the app container before replacing or deleting a
sideloaded build.

## Open a `.blend` document

Open a `.blend` from Files and choose Blender in the share or Open In sheet.
iOS routes the security-scoped document to the running Blender session. You can
also use Blender's normal **File > Open** command.

## Add an external folder

1. Open Blender's file browser.
2. Tap the folder-plus button beside the close button.
3. Choose one folder in Files and tap **Open**.
4. Find the folder under **System** in Blender's file browser.

Blender stores a bookmark and restores the location after relaunch. Granting
the same folder again does not create duplicates. Cloud and third-party file
providers can take a moment to answer. Let the Files sheet dismiss on its own.

![Blender's iOS file browser with the folder grant button highlighted](/blender-ios-build/files/external-folder.webp)

If a provider revokes access, add the folder again. Moving the folder or signing
the app under a different identity can also invalidate its saved bookmark.

## Secondary windows

Blender uses secondary windows for the file browser, render display, preferences,
and some editor operations. Tap the round close button in the top-right corner,
or press `Command-W` on a hardware keyboard. Wait for a window to close before
opening the same type again.
