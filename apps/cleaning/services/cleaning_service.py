import os
import tempfile

import pandas as pd

from django.core.files import File
import pandas.api.types as ptypes

from apps.datasets.models import Dataset
from apps.cleaning.models import (
    CleaningJob,
    CleaningStatus,
)
from apps.core.services.data_preprocessing import DataPreprocessingService
from datetime import datetime

DATE_PARSING_MODES = {
    "auto",
    "day_first",
    "month_first",
}


def parse_date(value, parsing_mode="auto", day_first=True):
    """Parse one date value without destroying values that cannot be parsed.

    ``auto`` prioritises unambiguous ISO dates and then uses ``day_first`` to
    resolve dates such as ``10/01/2024``.  Explicit modes only accept their
    respective day/month ordering.  The caller receives the original value
    when parsing fails, which keeps a cleaning operation non-destructive.
    """

    if pd.isna(value):
        return pd.NA

    value = str(value).strip()

    if not value:
        return pd.NA

    if parsing_mode not in DATE_PARSING_MODES:
        raise ValueError(f"Unsupported date parsing mode: {parsing_mode}")

    iso_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S%z",
    ]
    day_first_formats = ["%d/%m/%Y", "%d-%m-%Y"]
    month_first_formats = ["%m/%d/%Y", "%m-%d-%Y"]

    if parsing_mode == "day_first":
        formats = iso_formats + day_first_formats
    elif parsing_mode == "month_first":
        formats = iso_formats + month_first_formats
    elif day_first:
        formats = iso_formats + day_first_formats + month_first_formats
    else:
        formats = iso_formats + month_first_formats + day_first_formats

    for fmt in formats:
        try:
            parsed = datetime.strptime(value, fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return value


class CleaningService:

    @staticmethod
    def load_dataframe(dataset):

        file_path = dataset.original_file.path

        if dataset.file_type == "csv":
            return pd.read_csv(file_path)

        if dataset.file_type == "xlsx":
            return pd.read_excel(file_path)

        raise ValueError(f"Unsupported file type: {dataset.file_type}")

    @staticmethod
    def remove_duplicates(df):

        rows_before = len(df)

        cleaned_df = df.drop_duplicates()

        rows_after = len(cleaned_df)

        duplicates_removed = rows_before - rows_after

        summary = {
            "rows_before": rows_before,
            "rows_after": rows_after,
            "duplicates_removed": duplicates_removed,
        }

        return cleaned_df, summary

    @staticmethod
    def handle_missing_values(df):

        missing_before = int(df.isnull().sum().sum())

        for column in df.columns:

            if ptypes.is_numeric_dtype(df[column]):

                median_value = df[column].median()

                df[column] = df[column].fillna(median_value)

            else:

                df[column] = df[column].fillna("Unknown")

        missing_after = int(df.isnull().sum().sum())

        filled_values = missing_before - missing_after

        summary = {"missing_values_filled": filled_values}

        return df, summary

    @staticmethod
    def export_cleaned_files(df, dataset):
        """Create CSV and XLSX artifacts for a completed cleaning job."""

        temporary_directory = tempfile.mkdtemp(prefix="datadoctor_cleaning_")
        csv_filename = f"{dataset.id}_cleaned.csv"
        xlsx_filename = f"{dataset.id}_cleaned.xlsx"
        csv_path = os.path.join(temporary_directory, csv_filename)
        xlsx_path = os.path.join(temporary_directory, xlsx_filename)

        df.to_csv(csv_path, index=False)
        df.to_excel(xlsx_path, index=False)

        return {
            "csv": (csv_filename, csv_path),
            "xlsx": (xlsx_filename, xlsx_path),
            "directory": temporary_directory,
        }

    @staticmethod
    def standardize_text(df, columns):

        standardized_columns = []

        for column in columns:

            if column in df.columns:

                df[column] = (
                    df[column]
                    .astype(str)
                    .str.strip()
                    .str.replace(r"\s+", " ", regex=True)
                    .str.title()
                )

                standardized_columns.append(column)

        summary = {
            "text_standardized": True,
            "standardized_columns": standardized_columns,
        }

        return df, summary

    @staticmethod
    def standardize_dates(
        df,
        columns,
        parsing_mode="auto",
        day_first=True,
    ):

        standardized_columns = []

        failed_columns = []
        parsing_statistics = {}

        for column in columns:

            if column in df.columns:

                try:

                    original_values = df[column].copy()
                    df[column] = df[column].apply(
                        parse_date,
                        parsing_mode=parsing_mode,
                        day_first=day_first,
                    )

                    non_empty_values = original_values.notna()
                    parsed_values = non_empty_values & df[column].astype(
                        "string"
                    ).str.match(
                        r"^\d{4}-\d{2}-\d{2}$",
                        na=False,
                    )
                    invalid_values = non_empty_values & ~parsed_values

                    parsing_statistics[column] = {
                        "values_processed": int(non_empty_values.sum()),
                        "values_parsed": int(parsed_values.sum()),
                        "invalid_values_preserved": int(invalid_values.sum()),
                    }

                    standardized_columns.append(column)

                except Exception:

                    failed_columns.append(column)

        summary = {
            "date_standardized": True,
            "date_parsing_mode": parsing_mode,
            "standardized_date_columns": standardized_columns,
            "failed_date_columns": failed_columns,
            "date_parsing_statistics": parsing_statistics,
        }

        return df, summary

    @staticmethod
    def fix_data_types(df, columns):

        converted_columns = {}
        failed_columns = []

        for column in columns:

            if column in df.columns:

                try:

                    # Convert values to numeric
                    numeric_series = pd.to_numeric(df[column], errors="coerce")

                    # Remove nulls for validation
                    non_null = numeric_series.dropna()

                    # Skip if entire column failed conversion
                    if len(non_null) == 0:
                        failed_columns.append(column)
                        continue

                    # Check whether all values are whole numbers
                    if (non_null % 1 == 0).all():

                        # Nullable integer type supports missing values
                        df[column] = numeric_series.astype("Int64")

                        converted_columns[column] = "integer"

                    else:

                        df[column] = numeric_series.astype(float)

                        converted_columns[column] = "float"

                except Exception:

                    failed_columns.append(column)

        summary = {
            "data_types_corrected": True,
            "converted_columns": converted_columns,
            "failed_columns": failed_columns,
        }

        return df, summary

    @staticmethod
    def run_cleaning(dataset, config):

        cleaning_summary = {}

        job = CleaningJob.objects.create(
            dataset=dataset,
            status=CleaningStatus.RUNNING,
            selected_actions=config,
        )

        try:

            dataset.status = "CLEANING"
            dataset.save(update_fields=["status", "updated_at"])

            df = CleaningService.load_dataframe(dataset)

            df = DataPreprocessingService.preprocess_dataframe(df)

            if config.get("remove_duplicates"):
                df, duplicate_summary = CleaningService.remove_duplicates(df)

                cleaning_summary.update(duplicate_summary)

            if config.get("handle_missing_values"):
                df, missing_summary = CleaningService.handle_missing_values(df)

                cleaning_summary.update(missing_summary)

            text_config = config.get("standardize_text", {})
            if text_config.get("enabled"):
                df, text_summary = CleaningService.standardize_text(
                    df, text_config.get("columns", [])
                )

                cleaning_summary.update(text_summary)

            date_config = config.get("standardize_dates", {})
            if date_config.get("enabled"):
                df, date_summary = CleaningService.standardize_dates(
                    df,
                    date_config.get("columns", []),
                    parsing_mode=date_config.get("parsing_mode", "auto"),
                    day_first=date_config.get("day_first", True),
                )

                cleaning_summary.update(date_summary)

            datatype_config = config.get("fix_data_types", {})
            if datatype_config.get("enabled"):

                df, datatype_summary = CleaningService.fix_data_types(
                    df, datatype_config.get("columns", [])
                )

                cleaning_summary.update(datatype_summary)

            exported_files = CleaningService.export_cleaned_files(df, dataset)

            csv_filename, csv_path = exported_files["csv"]
            xlsx_filename, xlsx_path = exported_files["xlsx"]

            with open(csv_path, "rb") as cleaned_csv_file:
                job.cleaned_csv_file.save(
                    csv_filename,
                    File(cleaned_csv_file),
                    save=False,
                )
            # ``cleaned_file`` is retained for jobs created before Phase 3.
            # Point it at the CSV artifact instead of storing the same file twice.
            job.cleaned_file.name = job.cleaned_csv_file.name
            with open(xlsx_path, "rb") as cleaned_xlsx_file:
                job.cleaned_xlsx_file.save(
                    xlsx_filename,
                    File(cleaned_xlsx_file),
                    save=False,
                )

            job.rows_before = cleaning_summary.get("rows_before", len(df))

            job.rows_after = cleaning_summary.get("rows_after", len(df))

            job.duplicates_removed = cleaning_summary.get("duplicates_removed", 0)

            job.cleaning_summary = cleaning_summary

            job.status = CleaningStatus.COMPLETED

            job.save()

            dataset.status = "COMPLETED"
            dataset.save(update_fields=["status", "updated_at"])

            os.remove(csv_path)
            os.remove(xlsx_path)
            os.rmdir(exported_files["directory"])

            return job

        except Exception:

            job.status = CleaningStatus.FAILED
            job.save()
            dataset.status = "FAILED"
            dataset.save(update_fields=["status", "updated_at"])
            raise
