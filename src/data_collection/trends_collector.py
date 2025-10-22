"""
Google Trends data collector for Quebec market analysis.
Collects search trend data for furniture, appliances, mattresses, and flooring sectors.
"""

import logging
import time
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

import yaml
import pandas as pd
from pytrends.request import TrendReq

from .database import TrendsDatabase


class QuebecTrendsCollector:
    """Collects and stores Google Trends data for Quebec market keywords."""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the trends collector.

        Args:
            config_path: Path to configuration YAML file
        """
        self.logger = self._setup_logging()
        self.config = self._load_config(config_path)
        self.db = TrendsDatabase(self.config['database']['path'])
        self.pytrends = TrendReq(
            hl=self.config['google_trends']['language'],
            tz=360  # UTC-6 for Quebec
        )

    def _setup_logging(self) -> logging.Logger:
        """Configure logging for the collector."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/trends_collector.log', mode='a')
            ]
        )
        # Create logs directory if it doesn't exist
        Path('logs').mkdir(exist_ok=True)
        return logging.getLogger(__name__)

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.logger.info(f"Configuration loaded from {config_path}")
        return config

    def collect_keyword_data(
        self,
        keyword: str,
        category: str,
        timeframe: Optional[str] = None
    ) -> Optional[pd.DataFrame]:
        """
        Collect Google Trends data for a single keyword.

        Args:
            keyword: Search term to collect data for
            category: Category (meubles, electromenagers, matelas, couvre_planchers)
            timeframe: Time period (e.g., 'today 12-m', 'today 3-m')

        Returns:
            DataFrame with date index and interest values, or None if failed
        """
        if timeframe is None:
            timeframe = self.config['google_trends']['timeframe']

        try:
            self.logger.info(f"Collecting data for '{keyword}' ({category})")

            # Build payload
            self.pytrends.build_payload(
                kw_list=[keyword],
                geo=self.config['google_trends']['geo'],
                timeframe=timeframe
            )

            # Get interest over time
            data = self.pytrends.interest_over_time()

            if data.empty or keyword not in data.columns:
                self.logger.warning(f"No data returned for '{keyword}'")
                return None

            # Clean data
            data = data[[keyword]]  # Keep only the keyword column
            data.index.name = 'date'

            self.logger.info(f"Successfully collected {len(data)} records for '{keyword}'")
            return data

        except Exception as e:
            self.logger.error(f"Error collecting data for '{keyword}': {e}")
            return None

    def collect_category(self, category: str, delay: Optional[int] = None) -> Dict:
        """
        Collect data for all keywords in a category.

        Args:
            category: Category name (meubles, electromenagers, etc.)
            delay: Seconds to wait between requests (respects rate limits)

        Returns:
            Dictionary with collection statistics
        """
        if delay is None:
            delay = self.config['collection']['delay_between_requests']

        if category not in self.config['keywords']:
            self.logger.error(f"Category '{category}' not found in config")
            return {'success': False, 'error': 'Category not found'}

        keywords = self.config['keywords'][category]
        total_records = 0
        successful_keywords = []
        failed_keywords = []

        self.logger.info(f"Starting collection for category: {category}")
        self.logger.info(f"Keywords to collect: {len(keywords)}")

        for keyword in keywords:
            try:
                # Collect data
                data = self.collect_keyword_data(keyword, category)

                if data is not None:
                    # Store in database
                    records = self.db.insert_trends_data(keyword, category, data)
                    total_records += records
                    successful_keywords.append(keyword)
                else:
                    failed_keywords.append(keyword)

                # Respect rate limits
                time.sleep(delay)

            except Exception as e:
                self.logger.error(f"Failed to process '{keyword}': {e}")
                failed_keywords.append(keyword)

        # Log collection metadata
        success = len(failed_keywords) == 0
        self.db.log_collection(
            keywords=keywords,
            success=success,
            records_inserted=total_records,
            error_message=f"Failed: {failed_keywords}" if failed_keywords else None
        )

        stats = {
            'category': category,
            'total_keywords': len(keywords),
            'successful': len(successful_keywords),
            'failed': len(failed_keywords),
            'records_inserted': total_records,
            'failed_keywords': failed_keywords
        }

        self.logger.info(f"Collection complete for {category}: {stats}")
        return stats

    def collect_all_categories(self) -> Dict:
        """
        Collect data for all categories defined in config.

        Returns:
            Dictionary with overall statistics
        """
        self.logger.info("=" * 60)
        self.logger.info("Starting full collection run")
        self.logger.info("=" * 60)

        start_time = datetime.now()
        all_stats = []

        for category in self.config['keywords'].keys():
            stats = self.collect_category(category)
            all_stats.append(stats)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        overall_stats = {
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_seconds': duration,
            'categories_processed': len(all_stats),
            'total_keywords': sum(s['total_keywords'] for s in all_stats),
            'total_successful': sum(s['successful'] for s in all_stats),
            'total_failed': sum(s['failed'] for s in all_stats),
            'total_records': sum(s['records_inserted'] for s in all_stats),
            'category_stats': all_stats
        }

        self.logger.info("=" * 60)
        self.logger.info("Collection run completed")
        self.logger.info(f"Duration: {duration:.2f} seconds")
        self.logger.info(f"Total records inserted: {overall_stats['total_records']}")
        self.logger.info("=" * 60)

        return overall_stats

    def get_related_queries(self, keyword: str) -> Dict:
        """
        Get related queries for a keyword (useful for discovering new keywords).

        Args:
            keyword: Search term

        Returns:
            Dictionary with top and rising related queries
        """
        try:
            self.pytrends.build_payload(
                kw_list=[keyword],
                geo=self.config['google_trends']['geo']
            )

            related = self.pytrends.related_queries()

            if keyword in related:
                return {
                    'keyword': keyword,
                    'top': related[keyword]['top'],
                    'rising': related[keyword]['rising']
                }

        except Exception as e:
            self.logger.error(f"Error getting related queries for '{keyword}': {e}")

        return {'keyword': keyword, 'top': None, 'rising': None}

    def update_stale_data(self, days_threshold: int = 1) -> Dict:
        """
        Update keywords that haven't been collected recently.

        Args:
            days_threshold: Update if last collection is older than this many days

        Returns:
            Collection statistics
        """
        from datetime import timedelta

        self.logger.info(f"Checking for stale data (>{days_threshold} days old)")

        keywords_to_update = []
        cutoff_date = datetime.now() - timedelta(days=days_threshold)

        # Check each category
        for category, keywords in self.config['keywords'].items():
            for keyword in keywords:
                last_collection = self.db.get_latest_collection_date(keyword)

                if last_collection is None or last_collection < cutoff_date:
                    keywords_to_update.append((keyword, category))
                    self.logger.info(f"Keyword '{keyword}' needs update (last: {last_collection})")

        if not keywords_to_update:
            self.logger.info("All data is up to date!")
            return {'keywords_updated': 0, 'message': 'No updates needed'}

        # Update stale keywords
        self.logger.info(f"Updating {len(keywords_to_update)} keywords")

        total_records = 0
        for keyword, category in keywords_to_update:
            data = self.collect_keyword_data(keyword, category)
            if data is not None:
                records = self.db.insert_trends_data(keyword, category, data)
                total_records += records
            time.sleep(self.config['collection']['delay_between_requests'])

        return {
            'keywords_updated': len(keywords_to_update),
            'records_inserted': total_records
        }


if __name__ == "__main__":
    # Example usage
    collector = QuebecTrendsCollector()

    print("\n" + "=" * 60)
    print("Quebec Market Trends Collector")
    print("=" * 60)

    # Collect all categories
    stats = collector.collect_all_categories()

    print(f"\nCollection Summary:")
    print(f"  Categories: {stats['categories_processed']}")
    print(f"  Keywords: {stats['total_keywords']}")
    print(f"  Records: {stats['total_records']}")
    print(f"  Duration: {stats['duration_seconds']:.2f}s")
