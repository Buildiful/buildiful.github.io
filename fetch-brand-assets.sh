#!/usr/bin/env sh
# Optional convenience tool for refreshes of official branding from Buildiful's public repository.
set -eu
mkdir -p assets
BASE="https://raw.githubusercontent.com/Buildiful/music-player/main/assets"
for filename in buildiful-logo-white.png favicon-16x16.png favicon-32x32.png apple-touch-icon.png favicon.ico; do
  curl -fL --retry 2 "$BASE/$filename" -o "assets/$filename"
done
printf 'Updated official Buildiful assets.\n'
