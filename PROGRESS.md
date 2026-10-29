# Progress — October 29, 2026

## Completed research milestone

- Locked protocol in local Git (`7bbcf60`) before outcome download.
- Retrieved official CMS HCAHPS, unplanned hospital visits and general-information files; metadata, dates, dictionary and footnote crosswalk. Every download has an exact URL, UTC retrieval time and SHA-256.
- Audited 5,419 general-information facilities, 325,720 HCAHPS rows and 67,060 unplanned-visit rows. No duplicate relevant national keys. String IDs preserved.
- Extracted 140 Wisconsin facilities; 64 acute-care hospitals; 63 reliable discharge scores; zero numeric hospital-wide readmission outcomes; zero eligible pairs. All 64 acute-care outcomes carry suppression footnote 4, and all 64 periods differ. No model fit.
- National availability check: all 4,790 Hybrid_HWR scores are Not Available. No analytical expansion beyond Wisconsin.
- Reviewed RED full text, Hydoub full text and Siddiqui abstract; recorded additional overlapping studies and access limits. No novelty claim.
- Built an accessible static page, real-data threshold exploration, full exclusion funnel, source downloads and methods. All source and derived data are public hospital aggregates.
- Local data checks passed. Browser checked desktop and 390px mobile layout with no horizontal overflow. Thresholds return n=63, 52 and 64 with matching dot counts; accessible chart table works; no browser warnings/errors observed.

## Hosting status

- Account verified through GitHub connector: parsaara01-stack.
- Public repository created and verified: https://github.com/parsaara01-stack/after-the-discharge
- GitHub Pages is live: https://parsaara01-stack.github.io/after-the-discharge/
- First check/build/deploy run passed: https://github.com/parsaara01-stack/after-the-discharge/actions/runs/40937997445
- Verified HTTP 200 for the page, CSS, JavaScript, interactive data, summary, exclusion CSV and methods; each matched the local file SHA-256.
- Cloned the public repository into a fresh directory, reran all integrity checks and confirmed no derived-file differences.
- The connector could read the new repository but denied file writes. Browser upload plus a checksum-verified one-time workflow imported the public source; the source archive was removed from the final tree. No persistent credentials or account permission changes were needed.

## Evidence limits

The current public release cannot answer the association question. Suppressed rates are not zeros. Different year-long periods overlap but do not match. Survey administration changed during 2025; Discharge Information items persisted while modes/content elsewhere changed. Nonresponse, different patient populations, hospital confounding, reverse causation and ecological bias would limit even a matched observational study. This pilot excludes critical access hospitals and is not representative of all Wisconsin care.

## Next substantive work

Audit a pinned historical release for unsuppressed hospital-wide scores and compatible survey dates. Amend the protocol before inspecting historical associations. Check hybrid/claims definition differences and denominator eligibility. Only then apply the predeclared five-state expansion if necessary. No patient data or outreach is authorized or needed for the public-data redesign.
