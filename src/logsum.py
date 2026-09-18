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
        dt = datetime.fromisoformat(clean_str)
        return dt.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None

def main():
    parser = argparse.ArgumentParser(description="Summarise event logs.")
    parser.add_argument("-i", "--input", required=True, help="Path to input CSV")
    parser.add_argument("-o", "--output", default="summary.csv", help="Path to output CSV")
    args = parser.parse_args()

    # Handle missing input file explicitly (Exit 2)
    try:
        with open(args.input, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            if not fieldnames:
                rows = []
            else:
                rows = list(reader)
    except FileNotFoundError:
        sys.stderr.write(f"Error: Input file '{args.input}' not found.\n")
        sys.exit(2)
    except Exception as e:
        sys.stderr.write(f"Error reading input file: {e}\n")
        sys.exit(1)

    groups = {}

    for row in rows:
        # Normalise service
        service_raw = row.get("service", "")
        service = service_raw.strip().lower() if service_raw else ""

        # Normalise level (Missing level -> UNKNOWN)
        level_raw = row.get("level", "")
        if not level_raw or not level_raw.strip():
            level = "UNKNOWN"
        else:
            level = level_raw.strip().upper()

        # Parse timestamp
        dt = parse_iso_utc(row.get("timestamp", ""))

        group_key = (service, level)
        if group_key not in groups:
            groups[group_key] = {
                "count": 0,
                "first_seen": None,
                "last_seen": None
            }

        groups[group_key]["count"] += 1

        if dt is not None:
            if groups[group_key]["first_seen"] is None or dt < groups[group_key]["first_seen"]:
                groups[group_key]["first_seen"] = dt
            if groups[group_key]["last_seen"] is None or dt > groups[group_key]["last_seen"]:
                groups[group_key]["last_seen"] = dt

    # Write output summary
    try:
        with open(args.output, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["service", "level", "count", "first_seen", "last_seen"])

            for (service, level), data in sorted(groups.items()):
                first_seen_str = data["first_seen"].strftime("%Y-%m-%dT%H:%M:%SZ") if data["first_seen"] else ""
                last_seen_str = data["last_seen"].strftime("%Y-%m-%dT%H:%M:%SZ") if data["last_seen"] else ""
                writer.writerow([service, level, data["count"], first_seen_str, last_seen_str])
    except Exception as e:
        sys.stderr.write(f"Error writing output file: {e}\n")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()