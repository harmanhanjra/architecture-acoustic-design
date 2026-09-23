#!/bin/bash
set -euo pipefail

echo "Starting acoustic simulation (Ctrl+C to stop)..."
while true; do
    python simulation/generate_data.py
    sleep 5
done
