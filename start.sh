#!/bin/bash
# macOS / Linux: run ./start.sh to start the study app (opens your browser). Needs Python 3.8+.
cd "$(dirname "$0")" && exec python3 app/serve.py --open
