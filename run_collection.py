#!/usr/bin/env python3
"""
Simple script to run data collection for Quebec market trends.
Run this script to collect the latest Google Trends data.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_collection.trends_collector import QuebecTrendsCollector


def main():
    """Run the data collection process."""
    print("=" * 70)
    print("Quebec Market Trends - Data Collection")
    print("=" * 70)
    print()

    try:
        # Initialize collector
        print("Initializing collector...")
        collector = QuebecTrendsCollector()
        print("✓ Collector initialized\n")

        # Run collection
        print("Starting data collection...")
        print("This may take several minutes depending on the number of keywords.\n")

        stats = collector.collect_all_categories()

        # Display results
        print("\n" + "=" * 70)
        print("Collection Complete!")
        print("=" * 70)
        print(f"Categories processed: {stats['categories_processed']}")
        print(f"Total keywords: {stats['total_keywords']}")
        print(f"Successful: {stats['total_successful']}")
        print(f"Failed: {stats['total_failed']}")
        print(f"Records inserted: {stats['total_records']}")
        print(f"Duration: {stats['duration_seconds']:.2f} seconds")

        # Show category breakdown
        print("\nCategory Breakdown:")
        for cat_stat in stats['category_stats']:
            print(f"  • {cat_stat['category']}: {cat_stat['successful']}/{cat_stat['total_keywords']} keywords, "
                  f"{cat_stat['records_inserted']} records")

        print("\n✓ Data collection successful!")
        print("You can now run the dashboard: streamlit run src/dashboard/app.py")

        return 0

    except Exception as e:
        print(f"\n✗ Error during collection: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
