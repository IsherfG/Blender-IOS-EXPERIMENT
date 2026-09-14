---
title: Blender for iOS
description: Blender on iPhone and iPad, with touch controls and a few limits to know about.
template: splash
hero:
  tagline: Desktop Blender, with touch controls for iPhone and iPad.
  actions:
    - text: Read the limits first
      link: /blender-ios-build/limitations/
      icon: open-book
      variant: primary
    - text: Install Blender
      link: /blender-ios-build/install/
      icon: right-arrow
    - text: Learn the controls
      link: /blender-ios-build/controls/touch/
      icon: open-book
---

This is Blender 5.2.1 with touch controls for iPhone and iPad. You get the
desktop interface and work with ordinary `.blend` files.

## What doesn't work

Before bringing a project over, check what it needs.

- **Add-ons aren't a sure thing.** Some Python-only add-ons may work.
  Desktop binaries and add-ons that launch other programs won't.
  The newer Extensions installer also has an iOS blocker.
- **No OSL shaders or Hydra rendering.** Projects that depend on them need
  changes before you can use them here.
- **No VR or SpaceMouse support.**
- **Heavy scenes can close the app.** iOS can stop Blender when it runs out
  of memory. Save often, especially before rendering.

USD import and export are included, as is OpenVDB. Hydra rendering is the part
of the USD-related tooling that's missing.

Read [What doesn't work](/blender-ios-build/limitations/) for the full list,
including [how add-ons work](/blender-ios-build/limitations/#add-ons-and-extensions)
and what we haven't tested yet.

## What you can do

Model, edit materials, and work with your usual Blender files. Use touch,
a keyboard and mouse, or Apple Pencil. Workbench and EEVEE run through Metal,
and Cycles includes CPU rendering and a Metal option for compatible devices.

You can also type into fields with the iOS keyboard, open files from the Files
app, and give Blender access to folders outside its own storage.

![Blender running on iPad](/blender-ios-build/overview/blender-ipad.webp)

## Before you install

You'll need an arm64 iPhone or iPad running iOS or iPadOS 18 or newer.
Blender's desktop interface is a tight fit on a phone. Landscape gives you
more room; a keyboard and mouse help too.

Start with the [installation guide](/blender-ios-build/install/), then
learn the [touch controls](/blender-ios-build/controls/touch/).
For modeling, materials, animation, and other Blender tools, use the
[Blender Manual](https://docs.blender.org/manual/en/5.2/).
