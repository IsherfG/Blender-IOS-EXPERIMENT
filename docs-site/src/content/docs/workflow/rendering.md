---
title: Rendering
description: Choose a supported viewport and render engine on iOS.
---

## Viewport

Solid Workbench and EEVEE rendered shading use Blender's Metal backend. They are
the best starting points on every supported device. Large textures, dense
geometry, and compiled shaders can exceed iOS memory limits sooner than on a Mac.

## Cycles

Cycles CPU is the proven fallback and works in the release build. Open Render
Properties, choose Cycles, and select CPU when you want the most predictable
result. Start with a small output size and a low sample count.

Cycles Metal is built for physical devices with tier-2 argument buffers. It is
hidden on the iOS Simulator because that simulated GPU cannot compile the
bindless Cycles kernels. If Metal appears in your Cycles device preferences,
test it on a copy of the project before a long render.

## A sensible first render

1. Keep the startup cube and choose EEVEE.
2. Set the output to 512 by 512 and a low sample count.
3. Render one still image.
4. Save the `.blend`, close Blender, reopen it, and render again.
5. Increase scene size only after both passes succeed.

Long renders keep the device hot and iOS may terminate an app under memory
pressure. Save before rendering. CPU Cycles is correct but can be slow on a phone.
