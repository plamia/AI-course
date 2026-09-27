# Risk Register — Task T1

| Finding ID | Cause / Trigger | Blast Radius | Mitigation | Resolution | Owner | Revisit Date |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ADV-T1-01** | Array query param memory inflation (`?limit=10&limit=20...`) | Event-loop slowdown under high request concurrency | Truncate query parameter arrays to max 10 elements in `parseVal()` | **FIX-NOW** | Dev Team | 2026-03-27 |
| **ADV-T1-02** | Hexadecimal / Scientific notation query strings (`?page=0x10`) | Silent fallback to `page=1` instead of HTTP 400 error | Validate string via `/^\d+$/` regex prior to `parseInt()` | **ACCEPT-WITH-RISK** | Lead Arch | 2026-06-01 |