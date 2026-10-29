# After the Discharge

**Parsa Ara · Wisconsin feasibility pilot · October 29, 2026**

Can current CMS data support a fair comparison between hospital discharge-information scores and hospital-wide 30-day readmissions? In this snapshot, **no**: 64 Wisconsin acute-care hospitals have discharge scores (63 pass our minimum reliability rule), but all 64 hybrid hospital-wide readmission scores are unavailable with suppression footnote 4. Measurement periods also differ. **Eligible paired sample: 0. No association is estimated.**

- Site: https://parsaara01-stack.github.io/after-the-discharge/
- Repository: https://github.com/parsaara01-stack/after-the-discharge
- [Protocol](docs/protocol.md) · [Methods](docs/methods.md) · [Data dictionary](docs/data-dictionary.md) · [Evidence review](docs/evidence.csv)
- [Source manifest](data/source_manifest.json) · [Bounded snapshot manifest](data/snapshot_manifest.json) · [National integrity audit](data/national_audit.json) · [Full Wisconsin exclusion audit](data/derived/wisconsin_audit.csv)

## Run locally

Python 3.9+; no package installation or build step required:

```sh
python3 scripts/run.py
```

This reproduces the audit, runs data-integrity checks, refreshes downloadable site copies, and serves http://127.0.0.1:8027. The static page loads local JSON; serve over HTTP rather than opening index.html as a file. Stop with Ctrl-C.

For noninteractive checks: `python3 scripts/check.py`. For the analysis alone: `python3 scripts/analyze.py`.

## Reproduce the sources

The repository includes exact-column Wisconsin extracts for the selected measures and all listed Wisconsin facilities. These total hundreds of rows, not patient records. National originals (about 126 MB), dictionaries and official methods PDFs are retained in the originating local workspace and excluded from Git.

`python3 scripts/restore_sources.py` downloads the **pinned** URLs from the manifest and verifies SHA-256 before writing. `python3 scripts/freeze_snapshot.py` audits national unique keys and re-extracts Wisconsin. `python3 scripts/check.py` recomputes results. If a CMS file changes or disappears at its pinned URL, restoration fails explicitly; the committed bounded extract remains usable. To research a new catalog release, use `fetch_sources.py --refresh` only on a separate branch, then re-audit definitions, dates and protocol before analyzing associations. Refresh is not an automatic longitudinal update.

The local protocol was committed as `7bbcf60` before outcome retrieval. This is a local audit trail, not external preregistration. That protocol commit is preserved in the local repository; its source and timing are documented here even if the GitHub connector creates a separate remote commit history.

## Boundaries

Public hospital-level aggregates only. No patient records, recruitment, causal claim, hospital ranking or medical-care recommendation. This is a useful feasibility result, not a completed intervention study. Unavailable readmission rates are not zero. See methods for exclusions, 2025 survey changes, survey nonresponse, population mismatch and a historical-release redesign.

## Publishing and checks

GitHub Pages publishes **`/site` through GitHub Actions**, with a reproducibility check before deployment. See `.github/workflows/pages.yml`. Deployment is only confirmed by a completed Pages run and successful public HTTP response; see `PROGRESS.md` for the actual verified state. Source updates alone are not deployment proof.

Code: MIT, see LICENSE. CMS data and official documentation retain their original source terms; see source manifest. Literature is linked and briefly summarized, not redistributed.
