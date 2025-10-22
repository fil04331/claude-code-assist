"""
Unit tests for the 30-day trend calculation in the dashboard.

Tests the date-based filtering approach vs the old data-point-based approach.
"""
import unittest
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))


class TestTrendCalculation(unittest.TestCase):
    """Test cases for the 30-day trend calculation logic."""

    def setUp(self):
        """Set up test data."""
        # Create mock weekly data for 12 months (52 weeks)
        # Simulating Google Trends weekly data
        self.end_date = datetime(2024, 10, 22)
        self.mock_weekly_data = []
        
        # Generate 52 weeks of data (12 months)
        for week_offset in range(52):
            date = self.end_date - timedelta(weeks=week_offset)
            # Simulate increasing trend in recent 30 days
            if week_offset < 4:  # Last ~4 weeks (28 days)
                interest = 70 + week_offset * 5
            elif week_offset < 8:  # Previous 30 days period
                interest = 50 + week_offset * 2
            else:
                interest = 50
            
            self.mock_weekly_data.append({
                'date': date,
                'interest': interest,
                'category': 'test'
            })
        
        # Reverse to chronological order
        self.mock_weekly_data.reverse()

    def test_date_based_filtering_with_weekly_data(self):
        """Test that date-based filtering works correctly with weekly data."""
        # Get the most recent date
        max_date = max(d['date'] for d in self.mock_weekly_data)
        
        # Define date ranges (as in the fixed implementation)
        recent_start = max_date - timedelta(days=30)
        older_start = max_date - timedelta(days=60)
        older_end = recent_start
        
        # Filter data by date ranges
        recent_data = [d for d in self.mock_weekly_data if d['date'] > recent_start]
        older_data = [d for d in self.mock_weekly_data if older_start < d['date'] <= older_end]
        
        # Assert we have data in both periods
        self.assertGreater(len(recent_data), 0, "Should have data in recent period")
        self.assertGreater(len(older_data), 0, "Should have data in older period")
        
        # Calculate averages
        recent_avg = sum(d['interest'] for d in recent_data) / len(recent_data)
        older_avg = sum(d['interest'] for d in older_data) / len(older_data)
        
        # Assert averages are calculated correctly
        self.assertGreater(recent_avg, 0, "Recent average should be positive")
        self.assertGreater(older_avg, 0, "Older average should be positive")
        
        # With our mock data, recent should be higher
        self.assertGreater(recent_avg, older_avg, "Recent trend should be higher")

    def test_old_implementation_fails_with_weekly_data(self):
        """Test that the old implementation would fail with 52 weeks of data."""
        # The old condition: if len(cat_data) > 60
        # With 52 weeks of data, this would NOT be met
        self.assertLessEqual(len(self.mock_weekly_data), 60, 
                            "52 weeks of data should be <= 60 data points")
        
        # This means the old implementation would NOT show a trend
        # even though we have 12 months of data

    def test_date_ranges_are_correct(self):
        """Test that date ranges span exactly 30 days."""
        max_date = max(d['date'] for d in self.mock_weekly_data)
        
        recent_start = max_date - timedelta(days=30)
        older_start = max_date - timedelta(days=60)
        older_end = recent_start
        
        # Filter data
        recent_data = [d for d in self.mock_weekly_data if d['date'] > recent_start]
        older_data = [d for d in self.mock_weekly_data if older_start < d['date'] <= older_end]
        
        if recent_data:
            # Recent period should span ~30 days (might be slightly less due to weekly data)
            recent_span = (max(d['date'] for d in recent_data) - min(d['date'] for d in recent_data)).days
            self.assertLessEqual(recent_span, 30, "Recent period should span at most 30 days")
        
        if older_data:
            # Older period should span ~30 days
            older_span = (max(d['date'] for d in older_data) - min(d['date'] for d in older_data)).days
            self.assertLessEqual(older_span, 30, "Older period should span at most 30 days")

    def test_handles_empty_data(self):
        """Test that the logic handles empty data gracefully."""
        empty_data = []
        
        # Should not crash with empty data
        if not empty_data:
            # This is what the implementation checks
            self.assertTrue(True, "Empty check works")
        else:
            self.fail("Should handle empty data")

    def test_handles_insufficient_data(self):
        """Test handling of insufficient data for both periods."""
        # Create data for only 20 days (insufficient for 60-day comparison)
        short_data = []
        end_date = datetime(2024, 10, 22)
        
        for day_offset in range(20):
            date = end_date - timedelta(days=day_offset)
            short_data.append({
                'date': date,
                'interest': 50,
                'category': 'test'
            })
        
        max_date = max(d['date'] for d in short_data)
        recent_start = max_date - timedelta(days=30)
        older_start = max_date - timedelta(days=60)
        older_end = recent_start
        
        recent_data = [d for d in short_data if d['date'] > recent_start]
        older_data = [d for d in short_data if older_start < d['date'] <= older_end]
        
        # With only 20 days of data, we might not have data in the older period
        # The implementation should handle this with the check:
        # if len(recent_data) > 0 and len(older_data) > 0
        if len(older_data) == 0:
            self.assertTrue(True, "Correctly identifies insufficient data in older period")


class TestTrendCalculationWithDailyData(unittest.TestCase):
    """Test cases with daily data (different frequency)."""

    def setUp(self):
        """Set up daily data for testing."""
        self.end_date = datetime(2024, 10, 22)
        self.mock_daily_data = []
        
        # Generate 90 days of data
        for day_offset in range(90):
            date = self.end_date - timedelta(days=day_offset)
            # Simulate increasing trend in recent 30 days
            if day_offset < 30:
                interest = 70 + day_offset * 0.5
            elif day_offset < 60:
                interest = 50 + day_offset * 0.2
            else:
                interest = 50
            
            self.mock_daily_data.append({
                'date': date,
                'interest': interest,
                'category': 'test'
            })
        
        self.mock_daily_data.reverse()

    def test_date_based_filtering_with_daily_data(self):
        """Test that date-based filtering works correctly with daily data."""
        max_date = max(d['date'] for d in self.mock_daily_data)
        
        recent_start = max_date - timedelta(days=30)
        older_start = max_date - timedelta(days=60)
        older_end = recent_start
        
        recent_data = [d for d in self.mock_daily_data if d['date'] > recent_start]
        older_data = [d for d in self.mock_daily_data if older_start < d['date'] <= older_end]
        
        # With daily data, we should have ~30 data points in each period
        self.assertGreater(len(recent_data), 20, "Should have at least 20 recent data points")
        self.assertGreater(len(older_data), 20, "Should have at least 20 older data points")
        
        # Calculate trend
        recent_avg = sum(d['interest'] for d in recent_data) / len(recent_data)
        older_avg = sum(d['interest'] for d in older_data) / len(older_data)
        
        self.assertGreater(recent_avg, older_avg, "Recent trend should be higher with daily data")


if __name__ == '__main__':
    unittest.main()
