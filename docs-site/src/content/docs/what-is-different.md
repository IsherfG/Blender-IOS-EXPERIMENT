---
title: What is different from desktop Blender
description: iOS-specific behavior in this Blender 5.2 port.
---

The user interface and project format come from Blender 5.2.1. Most Blender
documentation applies unchanged. The port adds the following iOS behavior.

## Input

- A shared virtual cursor lets touch act like a relative trackpad.
- The cursor accelerates and wraps across all four window edges.
- Touch gestures expose left drag, right mouse, double-click, Undo, Redo, search,
  3D orbit and pan, and 2D editor navigation.
- Native text entry accepts full expressions and preserves Done or Cancel behavior.
- Hardware mouse, trackpad, keyboard, and Apple Pencil feed Blender's normal input events.

## Platform integration

- UIKit owns app and window lifecycle while Blender advances its normal event loop.
- MetalKit supplies the drawable size and presentation timing.
- Blender child windows have an iOS close control and `Command-W` shortcut.
- The Files picker grants external folders and restores security-scoped bookmarks.
- `.blend` documents can arrive through the iOS document-opening path.

## Runtime and rendering

- The app bundles CPython 3.13, NumPy, and zstandard in signable frameworks.
- Extensions download work moves to an in-process thread because iOS forbids child processes.
- Workbench and EEVEE use Metal.
- Cycles CPU is included. Cycles Metal is available only when the physical GPU meets its resource requirements.
- The release IPA contains both iPhone and iPad device families and no developer signature.

For standard tools, use the [Blender 5.2 Manual](https://docs.blender.org/manual/en/5.2/).
