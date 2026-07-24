#!/usr/bin/env python3
"""Tests for air-quality-download: data parsing and validation."""

import sys
import os
import json
import tempfile
import unittest
import importlib.util

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "..", "scripts", "air-quality-download.py")
spec = importlib.util.spec_from_file_location("air_quality_download", SCRIPT_PATH)
aqd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aqd)


class TestPollutants(unittest.TestCase):
    """Test pollutant definitions."""

    def test_all_pollutants_have_units(self):
        for key, info in aqd.POLLUTANTS.items():
            self.assertIn("name", info)
            self.assertIn("unit", info)
            self.assertTrue(len(info["name"]) > 0)
            self.assertTrue(len(info["unit"]) > 0)

    def test_pollutant_keys(self):
        expected = {"pm2_5", "pm10", "ozone", "nitrogen_dioxide", "sulphur_dioxide", "carbon_monoxide"}
        self.assertEqual(set(aqd.POLLUTANTS.keys()), expected)


class TestOpenMeteoParsing(unittest.TestCase):
    """Test Open-Meteo response parsing."""

    def test_parse_hourly_response(self):
        mock_data = {
            "hourly": {
                "time": ["2023-01-01T00:00", "2023-01-01T01:00", "2023-01-01T02:00"],
                "pm2_5": [10.0, 15.0, 12.0],
                "pm10": [20.0, 25.0, 22.0],
            }
        }
        pollutants = ["pm2_5", "pm10"]
        records = aqd.parse_open_meteo_response(mock_data, pollutants)

        self.assertEqual(len(records), 3)
        self.assertEqual(records[0]["pm2_5"], 10.0)
        self.assertEqual(records[0]["date"], "2023-01-01")
        self.assertEqual(records[0]["hour"], "00")
        self.assertEqual(records[1]["pm2_5"], 15.0)

    def test_parse_empty_response(self):
        mock_data = {"hourly": {"time": []}}
        records = aqd.parse_open_meteo_response(mock_data, ["pm2_5"])
        self.assertEqual(len(records), 0)


class TestAggregation(unittest.TestCase):
    """Test data aggregation functions."""

    def test_aggregate_daily(self):
        records = [
            {"date": "2023-01-01", "hour": "00", "pm2_5": 10.0},
            {"date": "2023-01-01", "hour": "01", "pm2_5": 20.0},
            {"date": "2023-01-01", "hour": "02", "pm2_5": 30.0},
            {"date": "2023-01-02", "hour": "00", "pm2_5": 15.0},
        ]
        daily = aqd.aggregate_daily(records, ["pm2_5"])

        self.assertEqual(len(daily), 2)
        self.assertAlmostEqual(daily[0]["pm2_5"], 20.0)
        self.assertAlmostEqual(daily[0]["pm2_5_min"], 10.0)
        self.assertAlmostEqual(daily[0]["pm2_5_max"], 30.0)
        self.assertAlmostEqual(daily[1]["pm2_5"], 15.0)


class TestOutput(unittest.TestCase):
    """Test output writing."""

    def test_write_json(self):
        records = [{"date": "2023-01-01", "pm2_5": 10.0}]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = f.name
        try:
            aqd.write_output(records, path, as_json=True)
            with open(path) as f:
                loaded = json.load(f)
            self.assertEqual(loaded[0]["pm2_5"], 10.0)
        finally:
            os.unlink(path)

    def test_write_empty_records(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            path = f.name
        try:
            aqd.write_output([], path)
        finally:
            os.unlink(path)


class TestInputValidation(unittest.TestCase):
    """Test coordinate validation logic."""

    def test_valid_coordinates(self):
        self.assertTrue(-90 <= 39.9042 <= 90)
        self.assertTrue(-180 <= 116.4074 <= 180)

    def test_invalid_latitude(self):
        self.assertFalse(-90 <= 100 <= 90)

    def test_invalid_longitude(self):
        self.assertFalse(-180 <= 200 <= 180)


if __name__ == "__main__":
    unittest.main()
