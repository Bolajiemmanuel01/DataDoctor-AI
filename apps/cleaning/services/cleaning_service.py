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
    def run_cleaning(dataset):

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

            df, duplicate_summary = (
                CleaningService.remove_duplicates(df)
            )

            df, missing_summary = (
                CleaningService.handle_missing_values(df)
            )

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

            job.rows_before = (
                duplicate_summary["rows_before"]
            )

            job.rows_after = (
                duplicate_summary["rows_after"]
            )

            job.duplicates_removed = (
                duplicate_summary["duplicates_removed"]
            )

            job.cleaning_summary = {
                **duplicate_summary,
                **missing_summary,
            }

            job.status = CleaningStatus.COMPLETED

            job.save()

            os.remove(output_path)

            return job

        except Exception:

            job.status = CleaningStatus.FAILED
            job.save()
            raise