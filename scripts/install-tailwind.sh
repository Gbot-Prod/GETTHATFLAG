#!/usr/bin/env sh
# Download the Tailwind CSS standalone CLI (no Node needed) into bin/.
set -eu

VERSION="v4.1.11"
cd "$(dirname "$0")/.."

case "$(uname -s)-$(uname -m)" in
  Linux-x86_64)  asset="tailwindcss-linux-x64" ;;
  Linux-aarch64) asset="tailwindcss-linux-arm64" ;;
  Darwin-arm64)  asset="tailwindcss-macos-arm64" ;;
  Darwin-x86_64) asset="tailwindcss-macos-x64" ;;
  *) echo "Unsupported platform: $(uname -s)-$(uname -m)" >&2; exit 1 ;;
esac

mkdir -p bin
curl -sSfL -o bin/tailwindcss \
  "https://github.com/tailwindlabs/tailwindcss/releases/download/${VERSION}/${asset}"
chmod +x bin/tailwindcss
echo "Installed Tailwind ${VERSION} to bin/tailwindcss"
