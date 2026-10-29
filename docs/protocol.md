# After the Discharge — protocol v1
Author: Parsa Ara. Locked October 29, 2026, before retrieving hospital outcome values. This is a time-stamped local protocol, not a registered clinical study.

Question: Across comparable Wisconsin acute care hospitals, is the percentage reporting receipt of discharge information associated with hospital-wide risk-standardized 30-day readmission rates?

Unit: hospital, joined on exact string CMS facility identifier. No patient-level linkage, causal effect, savings claim, hospital ranking or advice for selecting medical care.

Population: Hospital General Information records in Wisconsin with type exactly Acute Care Hospitals. Exclude critical access, psychiatric, children's, VA and other types to reduce structural noncomparability. Retain ownership for audit; no post hoc hospital exclusions based on scores.

Exposure: HCAHPS H_COMP_6_Y_P, percentage answering yes to the discharge-information composite; not a star rating or Care Transition composite. Preserve survey completions, response rate, flags, and measurement dates. Primary reliability requires at least 100 completed surveys and no exposure footnote other than blank. Treat suppression, Not Available, and all nonnumeric strings as missing, never zero. Document 2025 instrument/mode changes; do not append a prior release or pool time series.

Outcome: READM_30_HOSP_WIDE if present as the claims-based hospital-wide risk-standardized 30-day readmission percentage. If retired, audit Hybrid_HWR as a separately named hybrid hospital-wide risk-standardized readmission measure; never substitute condition-specific rates or ratios. Selection is based on construct and availability, before examining Wisconsin outcome values. Preserve denominator, CMS intervals, footnotes and dates.

Temporal eligibility: exact equality of exposure and outcome start/end dates is required for the primary cross-sectional association. If unequal, report a feasibility pilot, show the periods and their intersection, and withhold a primary association. Overlap does not make populations equivalent. Hybrid voluntary/suppressed/non-numeric outcomes cannot enter a model.

Sample rule: Wisconsin first. At least 60 fully eligible hospitals are required before any exploratory association is estimated; this is a stability threshold, not a formal power guarantee. If Wisconsin has fewer than 60, expand once to the predefined contiguous five-state group WI, IL, IA, MI, MN using identical eligibility and periods. If temporal matching fails at the dataset level, do not expand to repair it; publish feasibility findings. No search over states or measures for statistical significance.

Analysis if eligible: unweighted hospital-level Pearson correlation and OLS slope per 5 percentage-point discharge score, 95% pairs-bootstrap intervals (10,000 resamples, seed 20261029). Sensitivity: Spearman correlation, >=300 surveys, ownership-stratified summaries if each cell >=10. Report distributions, denominator, missingness and exclusion funnel first. No p-value headline; no adjusted causal model in this pilot. Confounding, differential response, ecological bias, measurement error and selection remain.

Feasibility fallback: exact counts at each sequential exclusion; outcome-specific missingness tokens and footnotes; duplicates and ID formatting; distributions in the audited Wisconsin acute-care cohort separately, with denominators; no paired outcome chart if temporal eligibility fails. Expansion and follow-up decisions must be documented.

Integrity: download full bounded national CMS files and metadata/dictionary; retain immutable source bytes with SHA-256, UTC retrieval times and CMS modified/released dates. Export bounded Wisconsin audit tables and aggregate summaries. Abort on duplicate facility/measure keys. Data are public hospital aggregates, with no patient records. Latest available means the catalog snapshot retrieved today, not a promise of future refresh.
