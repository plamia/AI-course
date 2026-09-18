#!/usr/bin/env python3
import sys
import csv
import argparse
from datetime import datetime, timezone

def parse_iso_utc(ts_str):
    """Parse ISO 8601 timestamp string to UTC datetime object. Returns None if malformed."""
    if not ts_str:
        return None
    try:
        clean_str = ts_str.strip()
        if clean_str.endswith('Z'):
            clean_str = clean_str[:-1] + '+00:00'
        return datetime.fromisoformat(clean_str).astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None

def process_row(row):
    """Extract and normalise service, level, and timestamp from a row."""
    service = row.get("service", "").strip().lower()
    
    level_raw = row.get("level", "").strip()
    level = level_raw.upper() if level_raw else "UNKNOWN"
    
    dt = parse_iso_utc(row.get("timestamp", ""))
    return service, level, dt

def read_events(filepath):
    """Read events from CSV file with error handling."""
    try:
        with open(filepath, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader) if reader.fieldnames else []
    except FileNotFoundError:
        sys.stderr.write(f"Error: Input file '{filepath}' not found.\n")
        sys.exit(2)
    except Exception as e:
        sys.stderr.write(f"Error reading input file: {e}\n")
        sys.exit(1)

def write_summary(filepath, groups):
    """Write summarised groups to output CSV."""
    try:
        with open(filepath, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["service", "level", "count", "first_seen", "last_seen"])

            for (service, level), data in sorted(groups.items()):
                first_seen = data["first_seen"].strftime("%Y-%m-%dT%H:%M:%SZ") if data["first_seen"] else ""
                last_seen = data["last_seen"].strftime("%Y-%m-%dT%H:%M:%SZ") if data["last_seen"] else ""
                writer.writerow([service, level, data["count"], first_seen, last_seen])
    except Exception as e:
        sys.stderr.write(f"Error writing output file: {e}\n")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Summarise event logs.")
    parser.add_argument("-i", "--input", required=True, help="Path to input CSV")
    parser.add_argument("-o", "--output", default="summary.csv", help="Path to output CSV")
    args = parser.parse_args()

    rows = read_events(args.input)
    groups = {}

    for row in rows:
        service, level, dt = process_row(row)
        group_key = (service, level)

        if group_key not in groups:
            groups[group_key] = {"count": 0, "first_seen": None, "last_seen": None}

        groups[group_key]["count"] += 1

        if dt is not None:
            if groups[group_key]["first_seen"] is None or dt < groups[group_key]["first_seen"]:
                groups[group_key]["first_seen"] = dt
            if groups[group_key]["last_seen"] is None or dt > groups[group_key]["last_seen"]:
                groups[group_key]["last_seen"] = dt

    write_summary(args.output, groups)
    sys.exit(0)

if __name__ == "__main__":
    main()