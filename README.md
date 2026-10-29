# After The Discharge

Parsa Ara — matched-year Wisconsin observational research.

Live: https://parsaara01-stack.github.io/after-the-discharge/

61 acute-care hospitals have reliable discharge scores and hospital-wide readmission rates for July 2022–June 2023. The primary correlation is -0.19; a five-point higher discharge score corresponds to -0.26 readmission percentage points (95% bootstrap interval -0.64 to +0.09). The stricter 300-survey subset is more negative. This is an uncertain descriptive association, not a causal result.

## Reproduce

Install `requirements.txt`, then run `python3 scripts/historical_analysis.py`. Inputs, source hashes and full results are in `data/historical/`. See `docs/protocol-v2.md` and `docs/historical-methods.md`. Serve `site/` with `python3 -m http.server 8027 --directory site`.

The original 2026 feasibility audit, protocol and scripts remain as history. `scripts/check.py` verifies that earlier snapshot and site link integrity; it is not the complete historical-analysis test. No patient records were used.

To rebuild the source extracts from CMS, run `python3 scripts/extract_historical.py`. To verify hashes, independent estimates and deterministic results, run `python3 scripts/verify_historical.py`.
