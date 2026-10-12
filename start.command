#!/bin/bash
# macOS: double-click to start the study app (opens your browser). Needs Python 3 (python.org or `xcode-select --install`).
cd "$(dirname "$0")" && exec python3 app/serve.py --open
