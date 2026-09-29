# 3D Modeling Thingy documentation media

This directory contains screenshots and short H.264 clips used by the public
documentation site. Keep each file below 10 MiB and the directory below 50 MiB.

The Astro source lives in `docs-site`. Its `publicDir` points here, so GitHub
Pages publishes these files without copying them into the site source tree.

## Recording sources

`text/text-entry.mp4` is a short, silent excerpt of the accepted iPad
`build_files/ios/maestro/input_polish.yaml` recording. The source is
`/Volumes/BlenderBuild/blender-ios/artifacts/20260823-input-polish/maestro-accepted/2026-08-23_023337/Blender iPad touch and keyboard polish/startRecording/blender-ios-input-polish.mp4`.
It shows the native keyboard, entry of `3+4`, and the committed `7 m` value.
The source flow passed Maestro 2.8.0 on the iPad Pro 13-inch (M5) simulator.

To reproduce the web version from that capture:

```sh
ffmpeg -i "SOURCE.mp4" -t 10.5 -vf 'fps=15,scale=1024:-2' -an \
  -c:v libx264 -preset medium -crf 28 -pix_fmt yuv420p \
  -movflags +faststart text/text-entry.mp4
```
