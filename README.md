# marc-osint-server

Public information searches for corroboration and fraud signals: news, obituaries, and DPDP-compliant social media signal checks.

## Status
ALL TOOLS MOCKED. Real integrations: news search via a commercial search API; social signal check requires PNB MetLife legal sign-off and the §13.6 permitted-platforms list (TBD).

## Tools

| Tool | Purpose | §  | Mock |
|---|---|---|---|
| `news_search(name, location, date_range)` | Public news lookup | §13.5 | Yes |
| `obituary_search(name, location)` | Obituary search | §13.5 | Yes |
| `social_signal_check(name, location, dob)` | Public social media signals (investigation trigger only) | §13.6 | Yes |

## DPDP compliance
The `social_signal_check` tool MUST log every query (search terms, platforms, profiles visited, findings) for DPDP audit. The mock returns a `dpdp_audit_id` to model this.

## Used by skills
A5 osint-news-search, A6 social-signal-check
