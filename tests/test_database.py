"""
Basic tests for database functionality.
"""

import pytest
import sys
from pathlib import Path
import tempfile
import pandas as pd
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_collection.database import TrendsDatabase


def test_database_creation():
    """Test database initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = TrendsDatabase(str(db_path))

        assert db_path.exists()
        print("✓ Database created successfully")


def test_insert_and_retrieve_data():
    """Test inserting and retrieving trends data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = TrendsDatabase(str(db_path))

        # Create sample data
        dates = pd.date_range(start='2024-01-01', periods=10, freq='D')
        data = pd.DataFrame({
            'test_keyword': range(10, 20)
        }, index=dates)

        # Insert data
        records = db.insert_trends_data('test_keyword', 'test_category', data)
        assert records == 10
        print(f"✓ Inserted {records} records")

        # Retrieve data
        retrieved = db.get_trends_data(keywords=['test_keyword'])
        assert len(retrieved) == 10
        assert 'test_keyword' in retrieved['keyword'].values
        print(f"✓ Retrieved {len(retrieved)} records")


def test_get_summary_stats():
    """Test summary statistics."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = TrendsDatabase(str(db_path))

        stats = db.get_summary_stats()
        assert 'total_records' in stats
        assert stats['total_records'] == 0
        print("✓ Summary stats working")


def test_backup_database():
    """Test database backup."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = TrendsDatabase(str(db_path))

        backup_path = db.backup_database(str(Path(tmpdir) / "backup.db"))
        assert Path(backup_path).exists()
        print(f"✓ Backup created at {backup_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("Running Database Tests")
    print("=" * 60)
    print()

    try:
        test_database_creation()
        test_insert_and_retrieve_data()
        test_get_summary_stats()
        test_backup_database()

        print()
        print("=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
