import os

import pandas as pd

from django.core.files import File
import pandas.api.types as ptypes

from apps.datasets.models import Dataset
from apps.cleaning.models import (
    CleaningJob,
    CleaningStatus,
)
from apps.core.services.data_preprocessing import (
    DataPreprocessingService
)
from datetime import datetime


def parse_date(value, day_first=True):

    if pd.isna(value):
        return pd.NA

    value = str(value).strip()

    formats = [
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(value, fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return pd.NA

class CleaningService:

    @staticmethod
    def load_dataframe(dataset):

        file_path = dataset.original_file.path

        if dataset.file_type == "csv":
            return pd.read_csv(file_path)

        if dataset.file_type == "xlsx":
            return pd.read_excel(file_path)

        raise ValueError(
            f"Unsupported file type: {dataset.file_type}"
        )

    
    @staticmethod
    def remove_duplicates(df):

        rows_before = len(df)

        cleaned_df = df.drop_duplicates()

        rows_after = len(cleaned_df)

        duplicates_removed = (
            rows_before - rows_after
        )

        summary = {
            "rows_before": rows_before,
            "rows_after": rows_after,
            "duplicates_removed": duplicates_removed,
        }

        return cleaned_df, summary


    @staticmethod
    def handle_missing_values(df):

        missing_before = int(
            df.isnull().sum().sum()
        )

        for column in df.columns:

            if ptypes.is_numeric_dtype(df[column]):

                median_value = (
                    df[column].median()
                )

                df[column] = (
                    df[column]
                    .fillna(median_value)
                )

            else:

                df[column] = (
                    df[column]
                    .fillna("Unknown")
                )

        missing_after = int(
            df.isnull().sum().sum()
        )

        filled_values = (
            missing_before - missing_after
        )

        summary = {
            "missing_values_filled": filled_values
        }

        return df, summary
    

    @staticmethod
    def export_cleaned_file(df, dataset):

        output_filename = (
            f"{dataset.id}_cleaned.csv"
        )

        output_path = (
            f"/tmp/{output_filename}"
        )

        df.to_csv(
            output_path,
            index=False
        )

        return output_filename, output_path


    @staticmethod
    def standardize_text(df, columns):

        standardized_columns = []

        for column in columns:

            if column in df.columns:

                df[column] = (
                    df[column]
                    .astype(str)
                    .str.strip()
                    .str.replace(
                        r'\s+',
                        ' ',
                        regex=True
                    )
                    .str.title()
                )

                standardized_columns.append(column)

        summary = {
            "text_standardized": True,
            "standardized_columns": standardized_columns,
        }

        return df, summary
    

    @staticmethod
    def standardize_dates(df, columns, day_first=True):

        standardized_columns = []

        failed_columns = []

        for column in columns:

            if column in df.columns:

                try:

                    df[column] = df[column].apply(parse_date)

                    standardized_columns.append(column)

                except Exception:

                    failed_columns.append(column)

        summary = {
            "date_standardized": True,
            "standardized_date_columns": standardized_columns,
            "failed_date_columns": failed_columns,
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
                    numeric_series = pd.to_numeric(
                        df[column],
                        errors="coerce"
                    )

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
        )

        try:

            df = CleaningService.load_dataframe(dataset)

            df = (
                DataPreprocessingService
                .preprocess_dataframe(df)
            )

            if config.get("remove_duplicates"):
                df, duplicate_summary = (
                    CleaningService.remove_duplicates(df)
                )

                cleaning_summary.update(duplicate_summary)

            if config.get("handle_missing_values"):
                df, missing_summary = (
                    CleaningService.handle_missing_values(df)
                )

                cleaning_summary.update(missing_summary)

            text_config = config.get("standardize_text", {})
            if text_config.get("enabled"):
                df, text_summary = (
                    CleaningService.standardize_text(
                        df,
                        text_config.get("columns", [])
                    )
                )

                cleaning_summary.update(text_summary)
            
            date_config = config.get("standardize_dates", {})
            if date_config.get("enabled"):
                df, date_summary = (
                    CleaningService.standardize_dates(
                        df,
                        date_config.get("columns", []),
                        day_first=date_config.get(
                            "day_first",
                            True
                        )
                    )
                )

                cleaning_summary.update(date_summary)
            
            datatype_config = config.get("fix_data_types", {})
            if datatype_config.get("enabled"):

                df, datatype_summary = (
                    CleaningService.fix_data_types(
                        df,
                        datatype_config.get("columns", [])
                    )
                )

                cleaning_summary.update(datatype_summary)

            output_filename, output_path = (
                CleaningService.export_cleaned_file(
                    df,
                    dataset
                )
            )

            with open(output_path, "rb") as cleaned_file:

                job.cleaned_file.save(
                    output_filename,
                    File(cleaned_file),
                    save=False
                )

            job.rows_before = cleaning_summary.get(
                "rows_before",
                len(df)
            )

            job.rows_after = cleaning_summary.get(
                "rows_after",
                len(df)
            )

            job.duplicates_removed = cleaning_summary.get(
                "duplicates_removed",
                0
            )

            job.cleaning_summary = cleaning_summary

            job.status = CleaningStatus.COMPLETED

            job.save()

            os.remove(output_path)

            return job

        except Exception:

            job.status = CleaningStatus.FAILED
            job.save()
            raise