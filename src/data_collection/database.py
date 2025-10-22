"""
Database manager for Quebec Market Trends data storage.
Uses SQLite for local storage of Google Trends data.
"""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd


class TrendsDatabase:
    """Manages SQLite database for trends data storage."""

    def __init__(self, db_path: str = "data/trends.db"):
        """
        Initialize database connection and create tables if needed.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self._init_database()

    def _init_database(self):
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Table for trends data
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trends_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    category TEXT NOT NULL,
                    date DATE NOT NULL,
                    interest INTEGER NOT NULL,
                    geo TEXT DEFAULT 'CA-QC',
                    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(keyword, date)
                )
            """)

            # Table for metadata about collections
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS collection_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    collection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    keywords_collected TEXT,
                    success BOOLEAN,
                    error_message TEXT,
                    records_inserted INTEGER DEFAULT 0
                )
            """)

            # Indexes for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_keyword_date
                ON trends_data(keyword, date)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_category_date
                ON trends_data(category, date)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_collected_at
                ON trends_data(collected_at)
            """)

            conn.commit()
            self.logger.info(f"Database initialized at {self.db_path}")

    def insert_trends_data(
        self,
        keyword: str,
        category: str,
        data: pd.DataFrame
    ) -> int:
        """
        Insert trends data for a specific keyword.

        Args:
            keyword: The search keyword
            category: Category (meubles, electromenagers, etc.)
            data: DataFrame with date index and interest values

        Returns:
            Number of records inserted
        """
        records_inserted = 0

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            for date, row in data.iterrows():
                try:
                    interest_value = int(row.get(keyword, row.iloc[0]))

                    cursor.execute("""
                        INSERT OR REPLACE INTO trends_data
                        (keyword, category, date, interest, geo)
                        VALUES (?, ?, ?, ?, ?)
                    """, (keyword, category, date.strftime('%Y-%m-%d'),
                          interest_value, 'CA-QC'))

                    records_inserted += 1

                except Exception as e:
                    self.logger.error(f"Error inserting data for {keyword} on {date}: {e}")

            conn.commit()

        self.logger.info(f"Inserted {records_inserted} records for '{keyword}'")
        return records_inserted

    def log_collection(
        self,
        keywords: List[str],
        success: bool,
        records_inserted: int = 0,
        error_message: Optional[str] = None
    ):
        """
        Log metadata about a collection run.

        Args:
            keywords: List of keywords collected
            success: Whether collection was successful
            records_inserted: Number of records added
            error_message: Error message if failed
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO collection_metadata
                (keywords_collected, success, error_message, records_inserted)
                VALUES (?, ?, ?, ?)
            """, (', '.join(keywords), success, error_message, records_inserted))
            conn.commit()

    def get_trends_data(
        self,
        keywords: Optional[List[str]] = None,
        category: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Retrieve trends data from database.

        Args:
            keywords: Filter by specific keywords
            category: Filter by category
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            DataFrame with trends data
        """
        query = "SELECT * FROM trends_data WHERE 1=1"
        params = []

        if keywords:
            placeholders = ','.join(['?' for _ in keywords])
            query += f" AND keyword IN ({placeholders})"
            params.extend(keywords)

        if category:
            query += " AND category = ?"
            params.append(category)

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

        query += " ORDER BY date, keyword"

        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=params)
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
            return df

    def get_latest_collection_date(self, keyword: str) -> Optional[datetime]:
        """
        Get the most recent collection date for a keyword.

        Args:
            keyword: The keyword to check

        Returns:
            Most recent collection datetime or None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT MAX(collected_at)
                FROM trends_data
                WHERE keyword = ?
            """, (keyword,))

            result = cursor.fetchone()[0]
            if result:
                return datetime.fromisoformat(result)
            return None

    def get_all_keywords(self) -> List[str]:
        """Get list of all keywords in database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT keyword FROM trends_data ORDER BY keyword")
            return [row[0] for row in cursor.fetchall()]

    def get_categories(self) -> List[str]:
        """Get list of all categories in database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM trends_data ORDER BY category")
            return [row[0] for row in cursor.fetchall()]

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics about the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total records
            cursor.execute("SELECT COUNT(*) FROM trends_data")
            total_records = cursor.fetchone()[0]

            # Unique keywords
            cursor.execute("SELECT COUNT(DISTINCT keyword) FROM trends_data")
            unique_keywords = cursor.fetchone()[0]

            # Date range
            cursor.execute("SELECT MIN(date), MAX(date) FROM trends_data")
            date_range = cursor.fetchone()

            # Last collection
            cursor.execute("""
                SELECT MAX(collection_date)
                FROM collection_metadata
                WHERE success = 1
            """)
            last_collection = cursor.fetchone()[0]

            return {
                'total_records': total_records,
                'unique_keywords': unique_keywords,
                'date_range': date_range,
                'last_successful_collection': last_collection
            }

    def backup_database(self, backup_path: Optional[str] = None):
        """
        Create a backup of the database.

        Args:
            backup_path: Path for backup file (default: data/backups/)
        """
        if backup_path is None:
            backup_dir = self.db_path.parent / "backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"trends_backup_{timestamp}.db"

        backup_path = Path(backup_path)
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as source:
            with sqlite3.connect(backup_path) as target:
                source.backup(target)

        self.logger.info(f"Database backed up to {backup_path}")
        return str(backup_path)

    def close(self):
        """Close database connection."""
        self.logger.info("Database connection closed")


if __name__ == "__main__":
    # Test database setup
    logging.basicConfig(level=logging.INFO)

    db = TrendsDatabase()
    print("Database initialized successfully!")
    print(f"Database location: {db.db_path}")

    stats = db.get_summary_stats()
    print("\nDatabase Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
