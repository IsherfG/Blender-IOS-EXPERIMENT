---
title: Blender for iOS
description: Install and use Blender 5.2 on iPhone and iPad.
template: splash
hero:
  tagline: The desktop Blender interface, Metal viewport, Python, and CPU rendering on iPhone and iPad.
  actions:
    - text: Install Blender
      link: /blender-ios-build/install/
      icon: right-arrow
      variant: primary
    - text: Learn the controls
      link: /blender-ios-build/controls/touch/
      icon: open-book
    - text: Download the latest IPA
      link: https://github.com/Shlok-Bhakta/blender-ios-build/releases/latest/download/Blender-iOS.ipa
      icon: download
---

This port keeps Blender's normal desktop interface and adds an iOS input layer.
It is not a simplified mobile editor. Projects remain normal `.blend` files.

![Blender running on iPad](/blender-ios-build/overview/blender-ipad.webp)

## What works

- Workbench and EEVEE viewports through Metal
- Cycles CPU rendering, plus a tier-2 Metal path for supported physical devices
- Touch controls with a relative virtual cursor
- Apple Pencil pressure, tilt, hover, and double tap
- Hardware keyboard, mouse, and trackpad input
- Native text entry for Blender fields, including expressions such as `3+4`
- Blender's Python 3.13 runtime, NumPy, and zstandard
- Files app folder grants and `.blend` document opening
- Closeable Blender child windows

Use the [Blender Manual](https://docs.blender.org/manual/en/5.2/) for modeling,
animation, materials, geometry nodes, and standard Blender tools. This site
documents installation and the parts that differ on iOS.

## Device support

The app targets arm64 devices running iOS or iPadOS 18 or newer. It has native
iPhone and iPad layouts and supports iPad windowing. Landscape is the practical
choice on iPhone. iPad supports landscape and portrait.
