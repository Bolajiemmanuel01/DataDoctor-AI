# AI Design & Explainability (POC guidance)

This document explains how the AI/recommendation layer is positioned in the POC, and how to evolve it into a production-capable, explainable recommendation engine.

## Current POC approach

- The repository uses a `RecommendationService` that applies deterministic heuristics based on dataset profile outputs (e.g., missing value counts, duplicate counts, column name hints) to produce cleaning suggestions. This is intentionally simple for a POC.

## Desired AI responsibilities

The AI layer should provide:

- High-quality, contextualized recommendations for cleaning actions per column.
- Confidence scores for each recommendation.
- Human-readable explanations (why this recommendation was made).
- Example rows demonstrating the issue and proposed fix.
- Learning from user feedback to improve recommendations over time.

## Input and output schema

Recommendation input (from `DatasetProfile`):

- `column_stats`: types, missing_pct, unique_count, sample_values, min/max/mean (numeric)
- `dataset_stats`: row_count, column_count, duplicate_count

Recommendation output (example):

{
  "column": "revenue",
  "issue": "missing_values",
  "recommended_action": "median",
  "confidence": 0.87,
  "explanation": "Revenue is numeric with 12% missing values; median preserves distribution.",
  "examples": {
    "before": ["", "100.0", "200.0"],
    "after_preview": ["150.0", "100.0", "200.0"]
  }
}

## Explainability

Provide a blended explanation combining rule-based signals and model-based feature importance:

- Top contributing signals (e.g., high missing_pct, numeric keywords in column name, low uniqueness).
- Show sample values that triggered the signal.

## Feedback loop

Capture user actions after a recommendation (approve/adjust/reject) and store as labelled examples. Periodically retrain model(s) using the accumulated data.

## Model choices (progressive)

1. Rule-based engine (POC) — deterministic heuristics. Low risk and explainable. Already implemented.
2. Lightweight supervised model — small classifier/regressor per issue type (e.g., missing-value strategy classifier). Use explainability tools (SHAP/LIME) to surface feature importance.
3. Ensemble/hybrid — rule-based pre-filter + ML ranking for priorities and confidence.

## Privacy and safety

- Anonymize or sample data used for model training.
- Provide opt-in for customers to contribute feedback for model improvements.

## POC → Prod steps for AI layer

1. Add structured recommendation schema and persist recommendations and user feedback to a training store.
2. Implement an offline retraining pipeline and store model versions with metadata.
3. Add explainability tooling and expose explanations in the UI.
4. Add monitoring for model drift and recommendation acceptance rates.
