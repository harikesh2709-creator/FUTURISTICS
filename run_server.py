"""
NTRO Signal Analyzer — Server Launcher
Starts the FastAPI server with uvicorn.
"""

import sys
import os

# Add backend to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

import uvicorn


def main():
    print("=" * 60)
    print("  NTRO SIGINT WORKSTATION — Signal Analysis Platform v1.0")
    print("  Problem Statement 26147 | Space Technology Theme")
    print("  National Technical Research Organisation (NTRO)")
    print("=" * 60)
    print()
    print("  Starting server at http://localhost:8000")
    print("  Press Ctrl+C to stop")
    print()

    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()
