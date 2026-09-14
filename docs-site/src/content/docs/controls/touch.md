---
title: Touch and gestures
description: Complete touch control map for Blender on iPhone and iPad.
---

Touch uses a virtual cursor. Your finger behaves like a trackpad, so it can move
the cursor without hiding the part of Blender you are trying to hit.

![The virtual cursor over Blender's 3D Viewport](/blender-ios-build/touch/virtual-cursor.webp)

## Pointer and clicks

| Gesture | Blender input | Use it for |
| --- | --- | --- |
| One-finger drag | Move the virtual cursor | Aim at buttons, fields, objects, sockets, and timeline controls. This does not hold a mouse button. |
| One-finger tap | Left click at the virtual cursor | Select or activate whatever is under the cursor. The tap position does not teleport the cursor. |
| Tap, then hold and drag | Left-button drag | Move sliders, drag nodes, box-select, operate gizmos, and perform other desktop click-drag actions. Hold the second touch for a moment before moving. |
| One-finger triple tap | Desktop double-click | Rename entries and activate controls that require a double-click. |
| Two-finger hold | Right-button press and drag | Open context menus with a hold and release. Keep holding and move to perform a right-button drag. The hold begins after about 0.3 seconds. |

The cursor accelerates when your finger moves quickly and stays precise for
short movements. It wraps at every edge. If it leaves the right side, it
reappears on the left. Top and bottom behave the same way. Blender transforms
that normally hide or capture the desktop cursor also preserve continuous
motion and return the cursor when the operation ends.

## Navigation by editor

| Gesture | 3D Viewport | Shader Editor, Geometry Nodes, and other 2D editors |
| --- | --- | --- |
| Two-finger drag | Orbit the view | Pan the canvas or scroll the region |
| Pinch | Zoom | Zoom |
| Three-finger drag | Pan the view | Reserved for the 3D Viewport mapping. Use two fingers to pan 2D editors. |

Two-finger drag and pinch can run together, so you can orbit and zoom without
lifting both fingers. The gesture applies to the editor under the virtual cursor.
Move the cursor into the Shader Editor before navigating its node canvas. The
same rule applies to the Outliner, timeline, Properties, and every other editor:
put the cursor over that editor before scrolling, panning, or zooming it.

## Commands

| Gesture | Command |
| --- | --- |
| Two-finger tap | Undo |
| Three-finger tap | Redo |
| Four-finger tap | Open Blender Search, the same command as `F3` |

Multi-finger taps must be quick and nearly stationary. A two-finger hold becomes
right mouse instead of Undo. A moving two-finger gesture becomes navigation.
