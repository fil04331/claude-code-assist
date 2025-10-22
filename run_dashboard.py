#!/usr/bin/env python3
"""
Simple script to launch the Streamlit dashboard.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Launch the Streamlit dashboard."""
    print("=" * 70)
    print("Quebec Market Trends - Dashboard Launcher")
    print("=" * 70)
    print()

    dashboard_path = Path(__file__).parent / "src" / "dashboard" / "app.py"

    if not dashboard_path.exists():
        print(f"✗ Error: Dashboard file not found at {dashboard_path}")
        return 1

    print(f"Launching dashboard from: {dashboard_path}")
    print()
    print("The dashboard will open in your default web browser.")
    print("Press Ctrl+C to stop the dashboard.")
    print("=" * 70)
    print()

    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(dashboard_path),
            "--server.port=8501",
            "--server.headless=true"
        ])

    except KeyboardInterrupt:
        print("\n\n✓ Dashboard stopped.")
        return 0

    except Exception as e:
        print(f"\n✗ Error launching dashboard: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
