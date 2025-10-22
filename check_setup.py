#!/usr/bin/env python3
"""
Quick script to verify that the installation is correct and all dependencies are available.
"""

import sys
from pathlib import Path


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"✗ Python {version.major}.{version.minor} detected. Python 3.8+ required.")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_modules():
    """Check that all required modules are installed."""
    required_modules = [
        ('streamlit', 'Streamlit'),
        ('pandas', 'Pandas'),
        ('plotly', 'Plotly'),
        ('pytrends', 'PyTrends'),
        ('yaml', 'PyYAML'),
        ('sqlite3', 'SQLite3'),
    ]

    all_ok = True
    for module_name, display_name in required_modules:
        try:
            __import__(module_name)
            print(f"✓ {display_name}")
        except ImportError:
            print(f"✗ {display_name} - not installed")
            all_ok = False

    return all_ok


def check_directories():
    """Check that necessary directories exist."""
    required_dirs = [
        'src/data_collection',
        'src/dashboard',
        'config',
        'tests',
        'docs'
    ]

    all_ok = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/ - missing")
            all_ok = False

    return all_ok


def check_config():
    """Check that config file exists."""
    config_path = Path('config/config.yaml')
    if config_path.exists():
        print(f"✓ config/config.yaml")
        return True
    else:
        print(f"✗ config/config.yaml - missing")
        return False


def main():
    """Run all checks."""
    print("=" * 70)
    print("Quebec Market Trends - Installation Check")
    print("=" * 70)
    print()

    print("Python Version:")
    python_ok = check_python_version()
    print()

    print("Required Modules:")
    modules_ok = check_modules()
    print()

    print("Project Structure:")
    dirs_ok = check_directories()
    print()

    print("Configuration:")
    config_ok = check_config()
    print()

    print("=" * 70)

    if python_ok and modules_ok and dirs_ok and config_ok:
        print("✓ All checks passed! You're ready to go.")
        print()
        print("Next steps:")
        print("  1. Collect data: python run_collection.py")
        print("  2. Launch dashboard: python run_dashboard.py")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print()
        print("Try running:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
