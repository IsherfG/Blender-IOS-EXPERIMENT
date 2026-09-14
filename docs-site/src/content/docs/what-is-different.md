---
title: What's different on iOS
description: The changes you'll notice when coming from desktop Blender.
---

The interface and project format come from Blender 5.2.1. Your usual Blender
knowledge still applies, but input and file access work differently here.

## Your finger moves a cursor

Dragging a finger moves the cursor like a trackpad. A tap clicks wherever that
cursor is. The cursor wraps around the screen edges so you can keep moving
during a long drag.

Gestures give you orbit, pan, zoom, right click, Undo, Redo, and Search.
The [touch guide](/blender-ios-build/controls/touch/) lists them all.

## You can use the iOS keyboard or your own

Tap into a field to edit it with the iOS keyboard. Expressions such as `3+4`
work in numeric fields.

A hardware keyboard, mouse, or trackpad gives you more familiar desktop
controls. Pencil supports pressure, tilt, and hover where the device provides
it. See [keyboard, mouse, and Pencil](/blender-ios-build/controls/keyboard-mouse-pencil/).

## Folders need permission

Open projects through Files or Blender's file browser. For a folder outside
Blender's own storage, use the folder-plus button to grant access. Blender
remembers that folder for later.

The file browser and other separate windows have a close button at the top
right. `Command-W` works too.
See [files and windows](/blender-ios-build/workflow/files-and-windows/).

## Some desktop workflows won't carry over

Blender includes Python, but add-ons that need desktop libraries or helper
programs won't work unchanged. The Extensions installer also has a blocker.
OSL, Hydra rendering, VR, and SpaceMouse support aren't available.

Read [What doesn't work](/blender-ios-build/limitations/) for those limits.
For Blender's ordinary tools, use the
[Blender Manual](https://docs.blender.org/manual/en/5.2/).
