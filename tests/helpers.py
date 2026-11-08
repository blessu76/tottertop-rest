"""Shared test setup: puts scripts/ on sys.path and exposes REPO."""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
