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

        return df, filled_values


    @staticmethod
    def remove_duplicates(
        dataset: Dataset
    ):

        job = CleaningJob.objects.create(
            dataset=dataset,
            status=CleaningStatus.RUNNING,
        )

        try:

            df = (
                CleaningService.load_dataframe(
                    dataset
                )
            )

            df = (
                DataPreprocessingService
                .preprocess_dataframe(df)
            )

            rows_before = len(df)

            cleaned_df = df.drop_duplicates()

            cleaned_df, missing_filled = (
                CleaningService.handle_missing_values(
                    cleaned_df
                )
            )

            rows_after = len(cleaned_df)

            duplicates_removed = (
                rows_before - rows_after
            )

            job.rows_before = rows_before

            job.rows_after = rows_after

            job.duplicates_removed = (
                duplicates_removed
            )

            output_filename = (
                f"{dataset.id}_cleaned.csv"
            )

            output_path = (
                f"/tmp/{output_filename}"
            )

            cleaned_df.to_csv(
                output_path,
                index=False
            )

            with open(
                output_path,
                "rb"
            ) as cleaned_file:

                job.cleaned_file.save(
                    output_filename,
                    File(cleaned_file),
                    save=False
                )

            job.cleaning_summary = {

                "duplicates_removed":
                    duplicates_removed,

                "rows_before":
                    rows_before,

                "rows_after":
                    rows_after,
                
                "missing_values_filled":
                    missing_filled,
            }

            job.status = (
                CleaningStatus.COMPLETED
            )

            job.save()

            os.remove(output_path)

            return job

        except Exception:

            job.status = (
                CleaningStatus.FAILED
            )

            job.save()

            raise