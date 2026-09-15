---
title: Rendering
description: Choosing a render engine and keeping larger scenes manageable.
---

## Start small

Try rendering the startup cube in EEVEE at 512 by 512 before opening a heavy
scene. It gives you a quick check that rendering works on your device.

Workbench solid shading and EEVEE use Metal. Big textures, dense meshes, and
rendered viewport shading can use a lot of memory, so save before switching
to a heavier scene or starting a render.

## Cycles

Cycles includes CPU rendering. It's a useful fallback if GPU rendering isn't
available or a scene gives you trouble. Choose Cycles in Render Properties,
then select CPU. Start with a small image and a low sample count.

Cycles also includes Metal support for compatible devices. It needs GPU
features that aren't available everywhere, so the option may not appear.
Try a short render before committing to a long one.

## What's missing

OSL shaders and Blender's Hydra render integration aren't available.
A project that depends on either will need changes.
See [What doesn't work](/blender-ios-build/limitations/) before bringing over
a more involved setup.

## Long renders

A long render can heat up the device, and iOS can close Blender if it uses too
much memory. Save your project first. If a render won't finish, try a smaller
image, fewer samples, or lower-resolution textures.
