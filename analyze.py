#!/usr/bin/env python3
"""Architecture + Acoustic Neuroscience blend — architecture-acoustic-design."""
import json
with open("data.json") as f:
    d = json.load(f)
print(f"=== {d['repo']} ===")
print(f"Blend: {d['blend']}")
for k, v in d['metrics'].items():
    print(f"  {k}: {v}")
