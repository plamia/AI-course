# spec.md — logsum CLI

## Goal
A tiny command-line tool that reads a synthetic `events.csv` log file,
groups events by service and level, counts them, and writes a summary
to `summary.csv`.

## Inputs
- CSV file with header row and columns: `timestamp, level, service, message`
- `timestamp`: ISO 8601 string (e.g. `2024-01-15T13:45:30Z`)
- `level`: log level string (e.g. `INFO`, `WARN`, `ERROR`)
- `service`: originating service name (e.g. `auth-service`)
- `message`: free-text description

## Outputs
- CSV file `summary.csv` with one row per group and columns:
  `service, level, count, first_seen, last_seen`
- Header row always written, even with zero data rows.

## Normalisation rules
- `service`: lowercased, surrounding whitespace trimmed.
- `level`: uppercased, surrounding whitespace trimmed.
- `timestamp`: parsed to UTC; original string not preserved.

## Grouping rule
- Group key is the tuple `(service, level)` after normalisation.
- Rows with the same normalised service and level form one group.

## Aggregation
- `count`: number of rows in the group.
- `first_seen`: earliest valid timestamp in the group (UTC, ISO 8601).
- `last_seen`: latest valid timestamp in the group (UTC, ISO 8601).

## Edge cases
- **Missing level:** grouped under `level = "UNKNOWN"`; still counted.
- **Malformed timestamp:** row counted; timestamp excluded from
  first_seen / last_seen.
- **Group with no valid timestamps:** first_seen / last_seen are empty strings.
- **Empty input (header only):** write header-only summary.csv; exit 0.
- **Missing input file:** error to stderr; exit 2.

## CLI
- Usage: `logsum --input events.csv --output summary.csv`
- `--input` / `-i`: path to input CSV (required).
- `--output` / `-o`: path to output CSV (default: `summary.csv`).
- Exit codes:
  - `0` — success
  - `1` — malformed input file
  - `2` — input file not found

## Out of scope
- Streaming or very large files that exceed memory.
- Log formats other than the defined CSV schema.
- Filtering by date range or service.
- Network, database, or cloud output.
- Configuration files or environment variables.

## Signed off
PAK — 18.09.2026

## Implementation notes
- **Timestamp resilience:** Decided to treat malformed timestamps as valid log occurrences for counting and grouping purposes, but omitted them from `first_seen` and `last_seen` calculations by storing `None` values rather than raising a parse error.