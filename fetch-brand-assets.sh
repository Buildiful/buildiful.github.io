#!/usr/bin/env bash
# Optional one-time local copy of official Buildiful assets from an existing public repository.
set -euo pipefail
mkdir -p assets
ROOT="https://raw.githubusercontent.com/Buildiful/music-player/main/assets"
for f in buildiful-logo-white.png favicon.ico favicon-16x16.png favicon-32x32.png apple-touch-icon.png; do
  echo "Fetching $f"
  curl --fail --location --silent --show-error "$ROOT/$f" --output "assets/$f"
done
echo "Brand assets copied into ./assets."
