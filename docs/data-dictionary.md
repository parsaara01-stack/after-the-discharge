# Data dictionary

All data are public hospital aggregates. Missing is not zero. CMS source column definitions were checked against the July 2026 Downloadable Database Dictionary, pp. 33, 80–81; CMS footnote crosswalk is included. See `data/source_manifest.json` for exact URLs, release dates, UTC retrieval times, byte counts and SHA-256 hashes. Original string identifiers, dates, flags and unavailable tokens are preserved in the bounded source files.

| Audit field | Meaning / type |
| --- | --- |
| facility_id | CMS Facility ID, six-character string; never parse as an integer. Join is exact, one-to-one after selecting one measure. It is not a patient identifier. |
| facility_name, city | CMS facility name and city at this snapshot; names are not join keys. |
| hospital_type, ownership | CMS general-information classifications. Eligibility requires type `Acute Care Hospitals`; ownership is retained but not adjusted for. |
| discharge_percent | Numeric `HCAHPS Answer Percent` for `H_COMP_6_Y_P`, a patient/mode-adjusted discharge-information top-box composite. Percentage from 0 to 100, rounded as published. Not a star rating, raw count, fraction of all discharged patients, or a measure of patient comprehension. |
| completed_surveys | Total completed HCAHPS surveys reported for the hospital and period. This is not the item-specific response denominator or the readmission denominator. |
| survey_response_percent | Hospital HCAHPS survey response rate, percentage; records nonresponse context. |
| exposure_footnote | `HCAHPS Answer Percent Footnote`; blank is unflagged. Code 6 cautions that fewer than 100 patients completed the survey. |
| survey_count_footnote | `Number of Completed Surveys Footnote`, preserved independently. |
| exposure_start, exposure_end | Inclusive source measurement dates, MM/DD/YYYY. Here October 1, 2024–September 30, 2025. |
| readmission_raw | Verbatim `Score` for `Hybrid_HWR`, here `Not Available`. |
| readmission_percent | Numeric score if available; null/empty here. Hybrid hospital-wide all-cause risk-standardized 30-day readmission rate; distinct from condition-specific measures, excess days or hospital return visit ratios. No score was analyzed in this pilot. |
| readmission_footnote, readmission_footnote_text | CMS flag and crosswalk text. All 64 acute-care records have code 4, “Data suppressed by CMS for one or more quarters.” The crosswalk does not give the underlying reason; do not infer poor hospital performance. |
| readmission_denominator_raw | CMS `Denominator`, retained verbatim; unavailable here. Never substitute HCAHPS completed surveys. |
| readmission_lower_raw, readmission_upper_raw | CMS interval bounds; unavailable here. Not estimated or replaced with zero. |
| outcome_start, outcome_end | Inclusive source measurement dates; July 1, 2024–June 30, 2025. |
| primary_reliable_exposure | Boolean: numeric exposure, >=100 completed surveys, blank discharge-score footnote. A pragmatic minimum from the protocol, not a guarantee of unbiased results. |
| exact_period_match | Boolean equality of both source dates. Independently false for all 64 acute-care hospitals. |
| eligible | Boolean satisfying all sequential protocol filters. False for all records in this release. |

`data/derived/wisconsin_audit.csv` contains all 140 general-information facilities, including reasons for exclusions. `site/pilot-data.json` includes only the 64 acute-care facilities and the aggregate audit. `data/snapshot/` contains CMS columns unaltered except CSV serialization, filtered to Wisconsin and the chosen measures. The snapshot manifest records each parent file hash and filter; these extracts are not original CMS national files.

`summary.json`: summaries are unweighted across hospitals; medians and ranges describe published hospital estimates, not Wisconsin patients. Sensitivity threshold 0 includes every numeric score; 100 and 300 also require blank exposure footnotes. No confidence interval for an association exists because there are no eligible outcome observations.
