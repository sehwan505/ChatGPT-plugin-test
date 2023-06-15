from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent
with open(os.path.join(BASE_DIR, "config.json"), "r") as f:
    config = json.load(f)