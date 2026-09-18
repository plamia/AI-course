# refactor-notes.md — Kata 5.6

## Removed by AI in the refactor
- **Inline loop logic abstracted into helper functions (`process_row`, `read_events`, `write_summary`).**
  - **AI reason:** To improve readability and modularity of the main function.
  - **My decision:** Keep removed (cleaner separation of concerns without altering normalisation or exception handling).
- **Explicit temporary variables for stripping/checking whitespace.**
  - **AI reason:** Streamlined method chaining (`row.get(...).strip().lower()`).
  - **My decision:** Keep removed, as safety checks on empty fields are still fully preserved.