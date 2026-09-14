---
title: Keyboard, mouse, and Apple Pencil
description: Use desktop input devices and Apple Pencil with Blender on iOS.
---

## Mouse and trackpad

iOS pointer input maps directly into Blender. Motion is absolute, scrolling uses
Blender's trackpad events, and the left, middle, and right buttons keep their
normal meanings. Button drags stay attached to the button that started them.

This means Blender's normal desktop instructions work with a mouse. Middle drag
navigates the 3D view, Shift plus middle drag pans, and right click opens context
menus. Trackpad scrolling and pinch gestures follow Blender's keymap for the
editor under the cursor.

The app draws its own Blender cursor and hides the iOS pointer over the viewport.
The cursor wraps across window edges, including when you use a mouse or trackpad.

## Hardware keyboard

The hardware keyboard sends Blender key presses, releases, Unicode text, and
left or right modifier keys. Standard Blender shortcuts work, including `G`,
`R`, `S`, `Tab`, `F3`, number-row keys, function keys, arrows, and numpad keys
when the keyboard provides them.

`Command-W` closes a secondary Blender window. The on-screen close button in the
top-right corner does the same thing.

When you edit a Blender field, iOS moves focus to the native text editor. Done
commits the value and Cancel restores the original value. Focus returns to the
Blender window afterward, so hardware keyboard shortcuts continue to work.

![Entering an expression with the native iPad keyboard](/blender-ios-build/text/text-entry.webp)

## Apple Pencil

Apple Pencil uses its absolute tip position instead of the relative finger
cursor. A tip tap is left click. A Pencil drag holds the left button and carries
pressure and tilt into Blender. Hover moves the cursor on supported iPads.

Pencil double tap sends right click at the current Pencil position.

Finger gestures can still navigate while Pencil owns the tablet state. The app
tracks only the active Pencil touch, which prevents another finger lifting from
ending pressure input.
