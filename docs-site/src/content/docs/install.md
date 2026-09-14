---
title: Install Blender
description: Install the unsigned Blender IPA with SideStore or another signer.
---

The release contains an unsigned IPA. Your sideloading tool signs it for your
device. You do not need Apple's paid developer program.

Blender requires iOS or iPadOS 18 or newer. The download is about 200 MiB, so
use a reliable Wi-Fi connection and leave enough free storage for extraction.

## SideStore with a free Apple Account

SideStore is the recommended free route. A free Apple Account signs apps for
7 days at a time. SideStore can refresh them before they expire.

1. Follow SideStore's official [prerequisites](https://docs.sidestore.io/docs/installation/prerequisites).
   Install LocalDevVPN, install iLoader on a computer, and connect the device by USB for initial setup.
2. Follow the official [SideStore installation guide](https://docs.sidestore.io/docs/installation/install).
   Use your own Apple Account when iLoader asks. Do not send the password to this project.
3. On the device, trust the developer app under **Settings > General > VPN & Device Management**.
4. Enable Developer Mode under **Settings > Privacy & Security** if iOS asks for it.
5. Connect LocalDevVPN whenever you install, update, or refresh an app.
6. Open this page in Safari on the device and use the button below.
7. After Blender installs, open SideStore's **My Apps** page and confirm that Blender shows a 7-day expiry. Refresh it once to prove the weekly path.

[Install the latest release in SideStore](sidestore://install?url=https%3A%2F%2Fgithub.com%2FShlok-Bhakta%2Fblender-ios-build%2Freleases%2Flatest%2Fdownload%2FBlender-iOS.ipa)

If the button does not open SideStore, download the IPA and choose it from
SideStore's **My Apps** tab.

[Download Blender-iOS.ipa](https://github.com/Shlok-Bhakta/blender-ios-build/releases/latest/download/Blender-iOS.ipa)

## Autoloader

Autoloader is another on-device signing route. Open the install link in Safari,
let Autoloader sign the IPA, then finish under **Settings > Installation**.

[Install the latest release with Autoloader](https://marginally-better-apps.github.io/Autoloader/?url=https%3A%2F%2Fgithub.com%2FShlok-Bhakta%2Fblender-ios-build%2Freleases%2Flatest%2Fdownload%2FBlender-iOS.ipa)

## Other sideloaders

AltStore and other IPA signers may work, but they are not part of this release's
validation matrix. Give the tool the unmodified `Blender-iOS.ipa`. Do not unpack
and rebuild it. The app contains many embedded frameworks that the signer must
sign.

## First launch

The initial launch can take longer while iOS verifies the app and Blender loads
its startup data. Start with the default scene. Move the cube, save a `.blend`,
close the app, reopen it, and load that file before committing serious work.
