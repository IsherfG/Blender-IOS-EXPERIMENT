---
title: Known limitations
description: Current platform and release limits for Blender on iOS.
---

- Blender requires an arm64 device running iOS or iPadOS 18 or newer.
- Free Apple Account signing expires after 7 days. SideStore must refresh the app.
- Removing or replacing a sideloaded app can remove its private container. Back up `.blend` files first.
- iPhone uses the full desktop interface on a small screen. Landscape and a hardware pointer help.
- iPad window size and placement follow iPadOS. The app does not force full screen on current iPadOS releases.
- iOS does not support Python child processes, so `multiprocessing.Process` is unavailable.
- USD, OpenVDB, Embree, OSL, and path guiding are not part of this release profile.
- Cycles CPU works but is slow. Cycles Metal requires a physical tier-2 GPU and may not appear on every device.
- The Simulator cannot validate Pencil pressure, device thermals, free-account signing, SideStore refresh, or real cloud file providers.
- Large scenes can hit iOS memory limits. Save before rendering or switching heavy viewport modes.
- The app currently uses one Blender session. Multi-scene UIKit session restoration is not implemented.
- External displays, every iPad window arrangement, and future foldable iPhone layouts do not have complete device coverage yet.

Report reproducible port bugs in the project's [GitHub issue tracker](https://github.com/Shlok-Bhakta/blender-ios-build/issues).
For normal Blender questions, use the [Blender Manual](https://docs.blender.org/manual/en/5.2/) and Blender community resources.
